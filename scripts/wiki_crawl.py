# -*- coding: utf-8 -*-
"""灰机wiki 增量爬取工具（rev1999-pack 维护用）

作用：从 res1999.huijiwiki.com 拉取「指定基准日之后」的新增/改动页面，
转成与本包一致的 Markdown（`# 标题` + `> 来源: URL` + `[图: URL]` 占位），
写入指定目录并生成 `00_索引.md` 与 `_manifest.json`。

用法：
    # 1) 增量模式：拉取基准日之后的全部新增页面（旧版对照用 --since）
    python wiki_crawl.py --since 2026-09-12T00:00:00Z --out data/更新_2026-09-25

    # 2) 指定页面
    python wiki_crawl.py --pages 德雷克 格林杜尔 --out data/更新_2026-09-25

    # 3) 只列变更不下载
    python wiki_crawl.py --since 2026-09-12T00:00:00Z --list-only

    # 4) 把「最近改动过的既有页面」按原名覆盖到镜像目录（用于刷新旧文件）
    python wiki_crawl.py --since 2026-09-12T00:00:00Z --refreshed

选项：
    --since ISO8601   基准时间（含），默认 2026-09-12T00:00:00Z
    --out DIR         输出目录（默认脚本同级 ../data/更新_临时）
    --pages ...       只抓这些页面（可多个）
    --types new,edit  增量模式下要抓的变更类型，默认 new
    --refreshed       抓「被编辑过的既有页面」而不是新增页面
    --list-only       只打印清单
    --force           覆盖已存在文件（默认跳过，便于断点续爬）
    --sleep SEC       请求最小间隔，默认 1.0（Cloudflare 限流时调大）

注：站点有 Cloudflare 防护，api.php 直连需要浏览器 UA + X-Requested-With +
Sec-Fetch-* 请求头（见 _http_get），否则返回 403。
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

API = 'https://res1999.huijiwiki.com/api.php'
WIKI = 'https://res1999.huijiwiki.com/wiki/'
HEADERS = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                   '(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'),
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': 'https://res1999.huijiwiki.com/wiki/%E9%A6%96%E9%A1%B5',
    'X-Requested-With': 'XMLHttpRequest',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}
_LAST = [0.0]
MIN_INTERVAL = 1.0
DEFAULT_SINCE = '2026-09-12T00:00:00Z'

# 站点页脚/导航噪音（块级 class 片段），转换时丢弃
DROP_CLASSES = ('mw-editsection', 'navbox', 'toc', 'noprint', 'mw-references-wrap',
                'reference', 'nomobile', 'mw-collapsible-toggle', 'huiji-edit',
                'printfooter', 'catlinks', 'mw-jump-link', 'mw-indicators')


# ---------------------------------------------------------------- HTTP
def api(params, retries=6, timeout=45):
    p = dict(params)
    p.setdefault('format', 'json')
    p.setdefault('formatversion', '2')
    url = API + '?' + urllib.parse.urlencode(p)
    delay = 4.0
    for _ in range(retries):
        gap = time.time() - _LAST[0]
        if gap < MIN_INTERVAL:
            time.sleep(MIN_INTERVAL - gap)
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                _LAST[0] = time.time()
                return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            _LAST[0] = time.time()
            if e.code in (403, 429, 500, 502, 503, 504):
                time.sleep(delay)
                delay = min(delay * 1.7, 40.0)
                continue
            raise
        except Exception:
            _LAST[0] = time.time()
            time.sleep(delay)
            delay = min(delay * 1.7, 40.0)
    raise RuntimeError('API 请求失败（重试耗尽）: ' + url[:160])


def recent_changes(since, types=('new',), namespace=0):
    """since 之后的变更（升序），types 过滤 new/edit。"""
    out, cont = [], {}
    for t in types:
        cont = {}
        while True:
            params = {
                'action': 'query', 'list': 'recentchanges',
                'rcnamespace': str(namespace), 'rclimit': '500',
                'rcdir': 'newer', 'rcstart': since, 'rctype': t,
                'rcprop': 'title|timestamp|ids|type|sizes|comment',
            }
            params.update(cont)
            d = api(params)
            out.extend(d.get('query', {}).get('recentchanges', []))
            if 'continue' in d:
                cont = d['continue']
            else:
                break
    seen, uniq = set(), []
    for c in sorted(out, key=lambda x: x['timestamp']):
        if c['title'] in seen:
            continue
        seen.add(c['title'])
        uniq.append(c)
    return uniq


def page_html(title):
    d = api({'action': 'parse', 'page': title, 'prop': 'text|revid'})
    if 'error' in d:
        return None, None
    return d['parse']['text'], d['parse'].get('revid')


# ---------------------------------------------------------------- HTML -> Markdown
BLOCK_TAGS = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'table', 'ul', 'ol',
              'blockquote', 'pre', 'hr'}
CONTAINER_TAGS = {'div', 'section', 'center', 'article', 'aside', 'figure',
                  'dl', 'dd', 'dt', 'tbody', 'thead', 'tfoot', 'tr'}


def _inline(el):
    """把元素渲染成一行内联文本（图片转 [图: URL] 占位）。"""
    parts = []
    if el.text:
        parts.append(el.text)
    for c in el:
        if not isinstance(c.tag, str):      # 注释 / PI 直接跳过
            if c.tail:
                parts.append(c.tail)
            continue
        if c.tag == 'img':
            src = c.get('src') or c.get('data-src') or ''
            if src:
                parts.append(f'[图: {src}]')
        elif c.tag == 'br':
            parts.append('\n')
        else:
            parts.append(_inline(c))
        if c.tail:
            parts.append(c.tail)
    return ''.join(parts)


def _has_block_child(el):
    for c in el.iter():
        if isinstance(c.tag, str) and c.tag in BLOCK_TAGS:
            return True
    return False


def _txt(s):
    s = s.replace('\u00a0', ' ')
    s = re.sub(r'\[\s*编辑\s*\]', '', s)
    s = re.sub(r'[ \t]+', ' ', s)
    return s.strip()


def _blocks(el, out):
    """把 DOM 节点树转成块级 Markdown 行。"""
    for c in el:
        if not isinstance(c.tag, str):      # 注释 / PI
            continue
        tag = c.tag
        cls = c.get('class') or ''
        if any(d in cls for d in DROP_CLASSES):
            continue
        if tag in ('script', 'style'):
            continue
        if tag == 'hr':
            continue
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            lvl = int(tag[1]) + 1  # wiki 页面标题是 h1，正文 h2 -> ##
            t = _txt(_inline(c))
            if t:
                out.append('#' * min(lvl, 6) + ' ' + t)
                out.append('')
        elif tag == 'p':
            t = _txt(_inline(c))
            if t:
                out.append(t)
                out.append('')
        elif tag == 'table':
            for tr in c.iter('tr'):
                cells = [_txt(_inline(td)) for td in tr
                         if isinstance(td.tag, str) and td.tag in ('td', 'th')]
                cells = [x for x in cells if x != '']
                if cells:
                    out.append('| ' + ' || '.join(cells) + ' |')
                    out.append('')
        elif tag in ('ul', 'ol'):
            for li in c.findall('li'):
                t = _txt(_inline(li))
                if t:
                    out.append('- ' + t)
            out.append('')
        elif tag in CONTAINER_TAGS:
            if _has_block_child(c):
                _blocks(c, out)
                tail = _txt(c.tail or '')
                if tail:
                    out.append(tail)
                    out.append('')
            else:
                t = _txt(_inline(c))
                if t:
                    out.append(t)
                    out.append('')
        else:
            t = _txt(_inline(c))
            if t:
                out.append(t)
                out.append('')


def convert(html, title):
    from lxml import html as LH
    doc = LH.fromstring(html)
    roots = doc.xpath('//div[contains(@class,"mw-parser-output")]')
    root = roots[0] if roots else doc.getroot()
    out = []
    _blocks(root, out)
    body = '\n'.join(out)
    body = re.sub(r'\n{3,}', '\n\n', body).strip()
    return f'# {title}\n\n> 来源:  {WIKI}{title}\n\n{body}\n'


# ---------------------------------------------------------------- 落盘
_BAD = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


def filename_for(title):
    return _BAD.sub('_', title) + '.md'


def main():
    ap = argparse.ArgumentParser(description='灰机wiki 增量爬取')
    ap.add_argument('--since', default=DEFAULT_SINCE)
    ap.add_argument('--out', default=os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', '更新_临时'))
    ap.add_argument('--pages', nargs='*', default=None)
    ap.add_argument('--types', default='new')
    ap.add_argument('--refreshed', action='store_true',
                    help='改为抓取「被编辑过的既有页面」')
    ap.add_argument('--list-only', action='store_true')
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--sleep', type=float, default=1.0)
    args = ap.parse_args()
    global MIN_INTERVAL
    MIN_INTERVAL = args.sleep

    if args.pages:
        items = [{'title': t, 'timestamp': '-', 'type': 'manual', 'revid': ''}
                 for t in args.pages]
        since = args.since
    else:
        types = ('edit',) if args.refreshed else tuple(args.types.split(','))
        items = recent_changes(args.since, types=types)
        since = args.since
        if args.refreshed:
            items = [c for c in items if c['type'] == 'edit']

    print(f'待抓取页面: {len(items)} 个（基准 {since}）')
    if args.list_only:
        for c in items:
            print(f"  {c['timestamp'][:19]}  {c['type']:5s}  {c['title']}")
        return 0

    os.makedirs(args.out, exist_ok=True)
    manifest, ok, skipped, failed = [], 0, 0, 0
    for i, c in enumerate(items, 1):
        title = c['title']
        fp = os.path.join(args.out, filename_for(title))
        if os.path.exists(fp) and not args.force:
            skipped += 1
            manifest.append({'title': title, 'file': os.path.basename(fp),
                             'bytes': os.path.getsize(fp), 'status': 'skip'})
            continue
        try:
            html, revid = page_html(title)
        except Exception as e:
            print(f'  [{i}/{len(items)}] 失败 {title}: {e}')
            failed += 1
            manifest.append({'title': title, 'file': None, 'status': 'fail',
                             'error': str(e)})
            continue
        if html is None:
            print(f'  [{i}/{len(items)}] 跳过（页面不存在）{title}')
            failed += 1
            manifest.append({'title': title, 'file': None, 'status': 'missing'})
            continue
        md = convert(html, title)
        with open(fp, 'w', encoding='utf-8', newline='\n') as f:
            f.write(md)
        ok += 1
        manifest.append({'title': title, 'file': os.path.basename(fp),
                         'bytes': len(md.encode('utf-8')), 'revid': revid,
                         'type': c['type'], 'timestamp': c['timestamp'],
                         'status': 'ok'})
        print(f'  [{i}/{len(items)}] ok  {title}  ({len(md)} 字符)')

    with open(os.path.join(args.out, '_manifest.json'), 'w', encoding='utf-8') as f:
        json.dump({'since': since, 'count': len(items), 'manifest': manifest},
                  f, ensure_ascii=False, indent=1)
    print(f'\n完成: 新增 {ok} / 跳过 {skipped} / 失败 {failed} -> {args.out}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
