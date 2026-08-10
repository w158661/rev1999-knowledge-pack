页面: 3周年/ARG解谜活动
URL: https://res1999.huijiwiki.com/wiki/3周年/ARG解谜活动
分类: 活动
============================================================

本文所介绍的解谜方法的作者请见「解谜参与者」；本维基仅将方法整理至本页。本文内容参照发布的视频写作。

本页面介绍了3周年时游戏官方推出的隐藏ARG（以现实世界为平台、融合虚拟元素的跨媒介互动解谜游戏，模糊了现实与虚构边界）解谜活动。

目录

1 解谜参与者
2 入口

2.1 刻录后的图片
2.2 物品信息
2.3 音频内容
2.4 4月28日官方发布的帖子与入口

3 Overview

3.1 Ⅰ
3.2 Ⅱ
3.3 Ⅲ
3.4 Ⅳ

3.4.1 第一部分
3.4.2 第二部分

3.5 Ⅴ
3.6 Mail

3.6.1 M.S.jpg
3.6.2 storm.wav
3.6.3 map.png

4 Role

4.1 R1-1
4.2 R1-2
4.3 R1-3
4.4 R1-4
4.5 R2-1
4.6 R2-2

5 Team

5.1 T1-1

5.1.1 Letter
5.1.2 Attachment
5.1.3 Note

5.2 T1-2
5.3 T1-3

6 Final

6.1 gate
6.2 Final1
6.3 Final2

6.3.1 信息整理
6.3.2 username
6.3.3 password

6.4 Final3

7 尾声

解谜参与者[编辑]

@玩家musicraft
@夜鸦kora
@しろ初衷
@翼天_筱羽OuO
@April狐久
@画圆圈的圈圈
@小猫络合物desuwa
@MivikQ
@于是我们向前思考
@逐渐归零
@时咨月
@olb_rb
@杰出维尔汀
竹山云海
以及其他所有群友

相关视频：
1999的解谜到底有多难？解谜过程解析
藏了整整一年的彩蛋！重返未来三周年终极谜题【重返未来解密01】
重返未来解密第二阶段，什么叫格蕾丝是关键线索？【重返未来解密02】
用音乐进行加密！重返未来的地图里究竟藏了什么？【重返未来解密03】
献给全体玩家的一封情书，重返未来到底有多浪漫？【重返未来解密04】
重返未来三周年解密，宣告破解！这个彩蛋，献给玩家！
入口[编辑]
当玩家完成3.6版本的前线观察室的解构进程任务，并刻录人们向何处去·机密卷轴后，会被提示：[FATAL] Error at Bit-0: The foundation is corrupted.（[致命错误] 0比特位出错：底层内核已损坏。），并附带图Enter-1的图片。

  图Enter-1人们向何处去·机密卷轴刻录后的图片
同时，会新解锁磁记录媒介■■■■■■■■收录了一段回忆的磁记录媒介。《■■■■■■■■》已经添加至氛围制造机。。

刻录后的图片[编辑]
该图片使用LSB（修改图片像素最末二进制位来隐藏文字信息的简易隐写方法）隐写了内容。

使用软件（例如StegSolve）解析图片的红色通道第0位（如图Enter-2 Ⅰ），能解析出新的图片（如Enter-2 Ⅱ）。  图Enter-2 Ⅰ用StegSolve软件反隐写的结果
  图Enter-2 Ⅱ解析出的新图片
这个图片的内容是Befunge的代码。它可简单被视作从网格的左上角开始，初始方向为向右，根据“> / < / ^ / v”分别对应右、左、上和下移动光标，读取文本。

物品信息[编辑]
对于评论中的密语：6861766566756E，解为ASCII码后可得havefun（玩的愉快）。
对于介绍中的密语，再对照使用两次评论中的密语：

06 0E 02 0D 0F 1B 09 00 04 04 00 5C 5C
68 61 76 65 66 75 6E 68 61 76 65 66 75

对两组异或运算(对二进制位运算，运算规则是相同得0、不同得1的)，再解为ASCII码：
6E 6F 74 68 69 6E 67 68 65 72 65 3A 29n  o  t  h  i  n  g  h  e  r  e  :  )

即：nothinghere:)（什么也没有:) ）。
该物品信息对核心关卡无实际意义。

音频内容[编辑]
该音频是SSTV（一种把图片转成音频音调、通过无线电慢速传送静态图片的技术）的传输结果。
使用软件（例如EasyPal）将其转回图片（如图Enter-3 Ⅰ），能解析出新的图片（如图Enter-3 Ⅱ）。

  图Enter-3 Ⅰ用EasyPal软件反转换的结果
  图Enter-3 Ⅱ解析出的新图片
该图片中的表格从左到右、从上到下阅读，是QWERTY键盘从一个字母开始，按一定方向规律依次按下形成的图片。但是，部分不符合按键规律的字母位置构成游戏中重要的元素“霍夫曼结”。（如图Enter-3 Ⅲ）。按逆时针顺序读取霍夫曼结边框上的文字（如图Enter-3 Ⅳ），能得到So we beat on, boats against the current, ceaselessly into the past（意为“于是我们奋力向前，逆水行舟，却不断被推回过去。”，语出《了不起的盖茨比》结尾）该图片将在Overview Ⅴ中被使用。

  图Enter-3 Ⅲ音频图片的上色解析图
  图Enter-3 Ⅳ按箭头顺序阅读表格
4月28日官方发布的帖子与入口[编辑]
2026年4月28日官方在社交媒体发布了如下帖子：

隐藏于历史角落的神秘组织，友人不为人知的遥远过去，你所好奇的和从未知晓的。

图片
解析
对应版本
对应方向

图中是一个左旋的石英

3.2
左

俄语（右侧，权力）

3.3
右

八卦中的震卦。中国古代为“坐北朝南，左手朝东，右手朝西”，“帝出乎震……震，东方也”（《说卦传》）—— 震主正东，即左。

3.4
左

摘自阿兹特克人所作的《波杜里尼手抄本》 。原图中人们都面向右侧。

3.5
右

双精度右移的指令图，图中所有数字整体向右移一位，对应右。

3.6
右

北半球西欧地区的等压线镜像图。图中展现了一个北半球低压中心，气旋逆时针向中心辐合，对应左

3.7
左

将其按顺序填入图Enter-2 Ⅱ的问号中，得到图Enter-4 Ⅰ。其根据箭头方向，可读出ETET-A-ETET A。但因Befunge后进先出的原则，与图片末尾向左的箭头，提示我们将文本逆序为A TETE-A-TETE（面对面的凑近交谈）。

  图Enter-4 Ⅰ解析出的新图片
将其添加到《重返未来：1999》的游戏官网后缀，即 https://re.bluepoch.com/atete-a-tete ，可进入游戏入口。

Overview[编辑]
Ⅰ[编辑]
Overview Ⅰ的网址是 https://re.bluepoch.com/atete-a-tete ；密码是ADancingStarBorn。界面如图Ov1 page。

  Ov1 pageOverview Ⅰ的界面
Overview Ⅰ的界面包含文本I do not know if you will emerge victorious in this final trial.（我不知道你能否在这场最终试炼中脱颖而出。）
同时，在页面右侧藏有不可见的文本：

[RX]255 250 257 323 336 339 335 "BORN" 255 240
[RX]255 250 257 337 326 322 324 326 "PEACE" 255 240
[RX]255 250 257 324 336 340 334 336 340 "COSMOS" 255 240
[RX]255 250 257 329 336 337 326 "HOPE" 255 240
[RX]255 250 257 341 339 342 326 "TRUE" 255 240
[RX]255 250 257 340 337 330 339 330 341 "SPIRIT" 255 240
[RX]255 250 257 322 325 354 367 "FATE" 255 240
[RX]255 250 257 334 342 340 330 324 "MUSIC" 255 240
[RX]255 250 257 333 330 328 329 341 "LIGHT" 255 240
[RX]255 250 257 333 326 328 326 335 325 "LEGEND" 255 240
[RX]255 250 257 334 346 341 329 "MYTH" 255 240
[RX]255 250 257 322 337 337 333 326 "APPLE" 255 240
[RX]255 250 257 339 326 333 330 324 "RELIC" 255 240
[RX]255 250 257 333 336 335 325 336 335 "LONDON" 255 240
[RX]255 250 257 340 330 333 326 335 341 "SILENT" 255 240
[RX]255 250 257 340 330 328 330 333 "SIGIL" 255 240
[RX]255 250 257 344 336 339 333 325 "WORLD" 255 240
[RX]255 250 257 328 322 333 322 345 346 "GALAXY" 255 240
[RX]255 250 257 337 340 346 324 329 "PSYCH" 255 240
[RX]255 250 257 336 322 340 330 340 "OASIS" 255 240
[RX]255 250 257 328 336 333 325 "GOLD" 255 240
[RX]255 250 257 341 330 334 326 "TIME" 255 240
[RX]255 250 257 322 324 326 "ACE" 255 240
[RX]255 250 257 356 362 367 "SPY" 255 240
[RX]255 250 257 328 329 336 340 341 "GHOST" 255 240
[RX]255 250 257 340 341 339 326 322 334 "STREAM" 255 240
[RX]255 250 257 324 322 340 341 333 326 "CASTLE" 255 240
[RX]255 250 257 339 336 324 332 "ROCK" 255 240
[RX]255 250 257 323 326 322 341 "BEAT" 255 240
[RX]255 250 257 337 342 339 326 "PURE" 255 240
[RX]255 250 257 334 336 325 340 "MODS" 255 240
[RX]255 250 257 332 335 330 328 329 341 "KNIGHT" 255 240
[RX]255 250 257 343 330 335 346 333 "VINYL" 255 240
[RX]255 250 257 330 340 333 322 335 325 "ISLAND" 255 240
[RX]255 250 257 339 322 330 335 "RAIN" 255 240
[RX]255 250 257 327 333 322 334 326 "FLAME" 255 240
[RX]255 250 257 360 340 373 354 "MOTH" 255 240
[RX]255 250 257 339 342 335 326 "RUNE" 255 240
[RX]255 250 257 323 333 342 326 "BLUE" 255 240
[RX]255 250 257 371 323 368 371 367 "STAGE" 255 240
[RX]255 250 257 340 334 330 333 326 "SMILE" 255 240
[RX]255 250 257 323 339 330 325 328 326 "BRIDGE" 255 240
[RX]255 250 257 335 330 328 329 341 "NIGHT" 255 240
[RX]255 250 257 343 336 330 325 "VOID" 255 240

文本右侧的英文词有：

BORN    诞生
PEACE   和平
COSMOS  宇宙
HOPE    希望
TRUE    真实
SPIRIT  灵魂
FATE    命运
MUSIC   音乐
LIGHT   光芒
LEGEND  传说
MYTH    神话
APPLE   苹果
RELIC   遗迹
LONDON  伦敦
SILENT  寂静
SIGIL   印记
WORLD   世界
GALAXY  星系
PSYCH   心灵
OASIS   绿洲
GOLD    黄金
TIME    时间
ACE     王牌
SPY     间谍
GHOST   幽灵
STREAM  溪流
CASTLE  城堡
ROCK    岩石
BEAT    节拍
PURE    纯粹
MODS    模组
KNIGHT  骑士
VINYL   黑胶
ISLAND  岛屿
RAIN    雨
FLAME   火焰
MOTH    飞蛾
RUNE    符文
BLUE    深蓝
STAGE   舞台
SMILE   微笑
BRIDGE  桥梁
NIGHT   黑夜
VOID    虚空

除此以外，页面中的输入框中的默认字符*****有规律地闪烁着。它的闪烁规律符合着摩斯密码，转换为明文得到RFC1097。检索相关内容，可得到一篇文章，其中的内容片段提示着我们257是关键解谜密钥：

1.  Command name and code.
SUBLIMINAL-MESSAGE        257

1. 指令名称及代码：
潜意识信息        257

可发现：除去共有的开头[RX]255 250 257和后缀255 240，其余的数字组数与后方的英文字母数一致，并且，将[RX]255 250 257之后的每个数字减去257，获得的对应ASCII编码与后面的英文词对应。
例如，[RX]255 250 257 323 336 339 335 "BORN" 255 240中的323 336 339 335每个数分别减去257得到66 79 82 78，对应ASCII码的B、O、R和N。
但是，"FATE"、"SPY"、"MOTH"和“STAGE”四个无法被解码。对这四个按上述方法解码后，解得文本ADan cin gSta rBorn
组合后的A Dancing Star Born（一个舞蹈明星的诞生）即为本关的密码。

Ⅱ[编辑]
Overview Ⅱ的网址是 https://re.bluepoch.com/atete-a-tete/Ft6Ap3x7 ；密码是She is the end, not the means。界面如图Ov2 page。Overview Ⅱ的界面包含一台老式电视机图片（如图Ov2）。解析过程如下：

  图Ov2 pageOverview Ⅱ的界面
  图Ov2Overview Ⅱ界面中的电视机
电视中的文本：

> SYSTEM RECOVERY INITIATED...>

QUERY: "Was that your goal to find her and end all this?"

[CORRUPTED_MEMORY_BLOCK_01]
RXQYVETBHRMARTWOAPBKL
OWPZQVFGHETUHXEKSKMLYVCJEDLNW
PQAETONDSFOF
TXMBVHEIEPRZA

> ERROR: NOISE DETECTED.
> AWAITING FILTER KEY...

> 系统恢复已启动……>
查询：“找到她并终结这一切，是你的目标吗？”
[损坏的内存块_01]
……
> 错误：检测到噪声干扰。
> 等待过滤器密钥……

在3.3版本前线观察室中对应有一份机密卷轴，两侧的摩斯密码字符数与电视机中CORRUPTED_MEMORY_BLOCK_01中的文本字符数一致。将其逐行对应：

RXQYVETBHRMARTWOAPBKL
···-·-·····------·-··
OWPZQVFGHETUHXEKSKMLYVCJEDLNW
-····-···--·-·-·--······-·-··
PQAETONDSFOF
···----·-·--
TXMBVHEIEPRZA
-····--·-·-·-

因为提示“过滤器”、“噪声”，尝试仅保留“-”对应的字母，得到：

YEARTWOAB
OVETHESKEL
ETONSOF
THEERA

即Year two above the skeletons of the era.（第二年的时代骸骨之上），提示着查看「《重返未来：1999》二周年纪念动画：旧世新生」46秒时的恐龙骨架。注意到视频左下角快速闪过了八帧不同的黑白方块，将黑色记为1、白色记为0，根据2.8版本剧情中的主要角色兀尔德为盲人，联系盲文字符表，按6个一组读取,按盲文字母阅读顺序从上往下从右往左排列（1对应凸0对应凹）。则有：

100011 001101 011101-> S H E
101011 100011 -> I S
100001 001101 011101 -> T H E
011101 010001 011001 -> E N D
101111 -> ,
010001 010101 100001 -> N O T 
100001 001101 011101-> T H E
010011 011101 011111 010001 100011 -> M E A N S

即She is the end, not the means（她是目的，而非手段）为本关的密码。

/* JS Minified */MathJax={tex:{inlineMath:[['$','$'],['\\(','\\)']]},svg:{fontCache:'global'}};/* JS Minified */
Ⅲ[编辑]
Overview Ⅲ的网址是 https://re.bluepoch.com/atete-a-tete/r5RLziw7 ；密码是To die but not perish。界面如图OV3 page。Overview Ⅲ的界面包含一个时钟（如图Ov3）。解析过程如下：

  图OV3 pageOverview Ⅲ的界面
  图Ov3Overview Ⅲ界面中的时钟。文件名为“time slips by.png”
时钟上写着How much time do you have left? tsvwqfotxstnqdwyb（你还剩下多少时间？）该图片的EXIF信息中，IFD0-Artist有内容Multiplied by the Celestial Cycle, shifted by the Earthly Branches（与周天相乘，与地支相移）。根据“相乘”和“相移”，能想到仿射密码（单表代换古典密码，结合了“加法密码”和“乘法密码”的原理）
其加密函数是$E(x)=(ax+b) \pmod{m}$ （a为相乘，b为相移，m是字母表长度，这里取26），对应的解密函数为 $D(x)=a^{-1}(x-b) \pmod{m}$
提示中反复提到的时间引导我们联想到《不老春》剧情。在对应的3.4版机密卷轴中，摩斯密码XIAN YAO LONGEVITY SEAL，把英文字母按顺序对应1到26数字后：
X  I  A  N  Y  A  O  L  O  N  G  E  V  I  T  Y  S  E  A  L24 09 01 14 25 15 01 12 15 14 07 05 22 09 20 25 19 05 01 12
所有数字之和为255。将其视为角度，代入到日晷中，其指向酉时。
酉时在地支顺位中排行10。
令a=255，b=10，再将时钟上的tsvwqfotxstnqdwyb每一位英文字母按顺序对应1到26数字，代入到仿射密码解码公式，得到To die but not perish，为本关的密码（意为“身殁而道存”）。

Ⅳ[编辑]
第一部分[编辑]
Overview Ⅳ的网址是 https://re.bluepoch.com/atete-a-tete/ubHuLHZP ；第一部分的密码是SILVER PIGMENT SECRET BYPRODUCT。界面如图Ov4-1 page。解析过程如下：

  图Ov4-1 pageOverview Ⅳ第一部分的界面
本关卡需要利用浏览器的“开发人员工具”（一般浏览器按F12或者Ctrl+Shift+I即可打开）完成。由HTTP404的提示可以在网页请求的请求标头（请求标头（Request Headers）是 HTTP 协议中，客户端向服务器发送请求时，附带在请求行之后的一组键值对信息。它用来告诉服务器关于客户端、请求内容、期望的响应格式等元数据。）中发现网页尝试获取的cookie中有四个值为空的"ofrenda"字段（“ofrenda”指墨西哥亡灵节期间在家中或墓地搭建的祭坛）。
在对应的3.5版机密卷轴中，其摩斯密码词组SILVER PIGMENT SECRET BYPRODUCT BYPRODUCT SECRET SILVER SILVER，可以看出右侧是部分重复的词
选择左侧的有效部分SILVER PIGMENT SECRET BYPRODUCT分别设为对应的cookie字段，即可进入第二部分，下面是一个设置cookie的方法示例（输入>右侧的同行代码即可）：

> console.log(document.cookie)
ofrenda1=; ofrenda2=; ofrenda3=; ofrenda4=
undefined
> document.cookie = "ofrenda1=Silver; path=/";
'ofrenda1=Silver; path=/'
> document.cookie = "ofrenda2=Pigment; path=/";
'ofrenda2=Pigment; path=/'
> document.cookie = "ofrenda3=Secret; path=/";
'ofrenda3=Secret; path=/'
> document.cookie = "ofrenda4=Byproduct; path=/";
'ofrenda4=Byproduct; path=/'

第二部分[编辑]
第二部分的密码是Not forever on earth, but briefly here。界面如图Ov4-2 page。解析过程如下：

  图Ov4-2 pageOverview Ⅳ第二部分的界面
Overview Ⅳ的界面包含文本Is it real, our elusive existence?  XX/13/17（我们缥缈的存在，是真实的吗？）。同时，网页源代码中包含注释：ofy:/13960/g2h1avpnjuy。将其用凯撒密码向后移位404，数字不变（相当于向前移位12或向后移位14），可以得到：ark:/13960/s2t1mhbzvgk。这是一个ARK类型（作为任何类型信息对象的持久标识符，类似于资源的“永久地址”）的URL。在前面加上标识符解析服务的前缀，前往 https://n2t.net/ark:/13960/s2t1mhbzvgk ，会被重定向到 https://archive.org/details/cantaresmexicano0000unse 。
“XX/13/17”是一个索引。在这本电子书中，查阅第XX章Songs（书本第185页）第13段（书本外侧的段号）第17行（书脊侧的行号）第一句话（如图Ov4-2 Ⅰ）[1]Not forever on earth, but briefly here（并非永驻尘世，只是短暂栖身于此），为本关的密码。

  图Ov4-2 ⅠOverview Ⅳ第二部分对应书页的局部
Ⅴ[编辑]
Overview Ⅴ的网址是 https://re.bluepoch.com/atete-a-tete/CeE2F42q ；密码是So we beat on, boats against the current, ceaselessly into the past。界面如图Ov5 page。Overview Ⅴ的界面包含文本Will you still press onward this time?（这次你还是要往前去吗？）。解析过程如下：

  图Ov5 pageOverview Ⅴ的界面
3.6版本的函电汇报共有5个版本，将每个版本背景图中的摩斯密码解码后，能得到(-1,-4)(-2,-3)(1,-4)(2,-3)四个坐标点。
在过去的四个关卡中，每个关卡均有一张隐藏图片，四张图片的文件名分别为：(0,-0.5)、(0,1)、(0,-2)、(0,3)，将其提取、提亮、增大对比度，并进行旋转后可拼出图Ov5 Ⅰ。
（图片名的坐标还可以确定图像的位置，纵坐标为正则在x轴上方，反之下方，数值较小的位于左侧，较大的位于右侧）

  图Ov5 Ⅰ四张隐藏图的拼合图
同时，在中心以100px为单位长度建立坐标系，并添加前面提到的8个坐标点，能看出这是霍夫曼结的轮廓
将其置于音频内容中sstv获得的图片Enter-3 Ⅱ并按霍夫曼结连线可以得到图Ov5 Ⅱ，和图Enter-3 Ⅳ一样阅读，得到

  图Ov5 Ⅱ四张隐藏图展现的霍夫曼结连线，并置于密码表上
So we beat on, boats against the current, ceaselessly into the past（于是，我们在激流中泛舟，逆行而上，直至退回到往昔岁月）
使用其作为密码进入Overview Mail部分。

Mail[编辑]
邮件的网址是 https://re.bluepoch.com/mail ；界面如图Ovm page。

  图Ovm page邮件的界面

HI!Sender: LEee bUPd Radio

Dear Timekeeper,
They say that with each new discovery, the shadow of the unknown only grows larger. A paradox you know all too well, is it not?
At this stage, we are willing to pull back the veil and offer you a glimpse into the unseen. We invite you to join us in looking for traces of those hidden in history's dark corners and hearing the unspoken tales of your closest companions. A chance to look back at your journey against the tides of time—this time, from a new perspective.
Yet the truth does not surrender itself easily, and unearthing it requires a keen mind. After all, a secret easily found is hardly a secret at all.

致司辰,
人们常说，每次新的发现，只会让扩大未知的阴影。你太熟悉这个悖论了，不是吗？
在此刻，我们要揭开帷幕，窥见那未曾显现的一隅。你我将一同，寻觅隐匿在历史角落中的踪迹，聆听你最亲密的伙伴未曾言说的故事。我们会追寻你逆时间洪流的脚步——以全新的视角。
但真相从不会轻易俯首，发掘真相需要敏锐的心智。毕竟，轻易就能找到的，称不上是秘密。

附件：
M.S.jpg
map.png
storm.wav

M.S.jpg[编辑]
  图Ovm-1M.S.jpg
图片如图Ovm-1。查看该图片文件的HEX编码，能看到png格式结束后的附加信息：IQAbGE0jFQoCHRUcAh0NSBoOB0gPGh0EGU8VDhkKBkgZBxFIHgoXBwMLVEo+GxsaAE1UAQNPFwcBAxUKAh0VHAQAGkgPCgAfCAoaSDcKGgdNDhoMTRscDU0pGx0DCxUcBAAaRmcmGkgZBxEBH08REB0KBgEAChocHk8HHR8dGx0DCx0GCk8CDR4cEQRNChobAhoYBQgBAERNHREbCA4GCwUKBhtNBhANAxsdDgQKEEgDAAINAU8YAQMKB0gCCVQBAx4BAR8WVAsCARcNHwEdBgpPBA0fHBsGDAMdHBRPFQYJTxkNAAAGEUNPIAAITxIBAwsdBgocVBoIHAEEGQYaD00JBgcATwAABBxUCR8KVAMDAAMGTQ4HSBkHEUg9BxscAhsVEAQcWmI5BxFIKwABBgkOAAECAVQdGQYYARcKEEgZBx0bTR0RGwgOBgsFTwAHTRsGCQQBVAYYAhEaAhoHSAUGEwABFlQMBBwXAR0DHQYIC1QJAwtUCQ8cGwQYGxEEFE8YBxQOGEgCHxEaDBsdHggcVAcfTwcYBAoHRE0YHRwFTzkbQ08nHB8OGg8IHVQbGQ4aDAQBE0gMHFQcBQpUGB8KEQUEAREGGU8HHQ4MERseQQ==

将其使用moth（“飞蛾”的英文单词）作为密钥，进行异或解谜，能解码出：Loop Laboratory was built after the second "Storm" in collaboration between Zeno and the Foundation.
In their experiments surrounding vessel ensoulment, researchers identified novel lines of inquiry concerning personality and memory. The findings resulting from this are known as the Phototaxis.
The Foundation utilized this research to train numerous highly disciplined and absolutely loyal operatives or spies, with Ms. Stranger standing as the preeminent success.（第二次“暴雨”后，由芝诺与基金会合作建成了“回环实验室”。在围绕血管赋灵开展的实验中，研究人员发现了有关人格与记忆的新研究方向。由此得出的研究成果被命名为“趋光性”。基金会利用这项研究，培养了大批纪律严明、绝对忠诚的特工或间谍，无名者女士便是其中最杰出的成功案例。）
将其中核心的两个词Phototaxis、stranger和无名者女士剧情中更常用的名字grace作为后缀填入深蓝互动官网，能得到：

role1-1： https://re.bluepoch.com/Phototaxis
role1-2： https://re.bluepoch.com/grace
role1-3： https://re.bluepoch.com/stranger
同时图片后面还附加有下面的字符画：
................................................................................
................................................................................
................................................................................
................................................................................
................................................................................
................................................................................
.......................................................f........................
.......................bv..............................1e.......................
........................f#............................fc........................
..........................de........................fg..........................
.............................fhi!...............jf&.............................
................................flam........fbc!................................
....................................d#....ef....................................
...................fgh................i!fj................fk&...................
......................la.............mfn!op.............fq......................
.......................fbc#.........fde..ghi.........fj!k.......................
...........................fabfcdefghfijklmfnpqrstuvw...........................
..............................ab!f......c.....fde@..............................
.................fg..h!fj!klm.........nfo@.........pqfs!tuv..vf.................
.......................wxfy...........z..f...........fbc@.......................
...................fde&...................g..............hi!f...................
.................fjk!lm....nf.@........o!.p......q.rf....st!uvf.................
..............fwx................yz..........!f@................ab..............
...........fcd#...................efg.h!if.jfk...................mfno...........
........fq!&........................sf!tuvw@........................xyfz........
.......!abc..........................dfegh!..........................fijk.......
.....fl.m!............nfo...pq........rfs@........tu....vf............wx.y!z....
....!f..a............bc.......d.......ef.g.......h.......!f............i..jk....
...f....l...........mn....5z...q......r!sf..........ke....xf................y...
..z!................!a...b!..cd.......ef!gh......ij..f@.................k...lf..
..5w.................nf.............op..q.r!..............st............u...bq..
....w!..xy............z@..........ab........cf..........de............f!..gf....
.........ifjklm......n!.opq@..rstu....v!wx....yza!..bcd#.ef......ghi!jk.........
...................l...m!no..........p....q..........rstu@..vb..................
..........................a.#2d2d9fghijk..lmnopqrstuv.wx........................
................................................................................
................................................................................
................................................................................
................................................................................
................................................................................

storm.wav[编辑]
  图Ovm-2storm.wav声道差分后的频谱图
将该音频的左、右声道差分，并获取频谱图，如图Ovm-2 Ⅰ。这是“依诺天使语”的文字，对照字母表，能得到drawing（需将对应V的字母映射为W），将其作为后缀填入深蓝互动官网，能得到：

role2-1： https://re.bluepoch.com/drawing
map.png[编辑]
  图Ovm-3map.png（本维基上传的图片有压缩）
如图Ovm-3，这是“黄金国”的一张地图。但其与原图对比，会发现上方罗盘的射线被修改了。将周围的射线从上方出发顺时针提取，重新排列并拼接，如图Ovm-3 Ⅰ，能看到organization，作为后缀填入深蓝互动官网，能得到：

team1-1： https://re.bluepoch.com/organization
  图Ovm-3 Ⅰmap.png拼接射线后的结果
Role[编辑]
R1-1[编辑]
Role 1-1的网址是 https://re.bluepoch.com/Phototaxis ；界面如图R1-1 page。界面包含一只飞蛾的图片（如图R1-1）和下面的文本：

  图R1-1 pageRole 1-1的界面
  图R1-1Role 1-1的插图，包含一只飞蛾，文件名为"moth.png"

Phototaxis in Study
Phototaxis is a complex technique used to surgically engrave a subject's skin and cerebral cortex with countless arcane incantations.
A psychological anchor is established within the subject's subconscious using this control system. It then facilitates the continuous rewriting of long-term memories in the subject's temporal lobe, allowing them to adopt hyper-realistic identities and memories tailored to specific mission parameters.
In the event of personality dissolution or total mental breakdown, the anchor also ensures that the subject retains a pure instinct for memory rewriting and command execution.

研究中的趋光术
趋光术是一种精密技术，通过神秘术在受术者的皮肤与大脑皮层上进行手术以镌刻。
该控制系统会在受术者的潜意识中构建一处心理锚点，进而持续改写其颞叶内的长期记忆，使其能够适配特定任务参数，拥有高度逼真的身份与记忆。
即便出现人格瓦解或精神彻底崩溃的情况，该锚点仍能确保受术者保留记忆改写与指令执行的纯粹本能。

R1-2[编辑]
Role 1-2的网址是 https://re.bluepoch.com/grace ；界面如图R1-2 page。界面包含历史上第一个“BUG”的图片（如图R1-2）。

  图R1-2 pageRole 1-2的界面
  图R1-2Role 1-2的插图，包含历史上第一个“BUG”，文件名为"grace.jpg"
1947年，因一只飞蛾卡在了第70号继电器触点间，产生了“第一个计算机Bug”。图片的相关记录原文“Relay #70 Panel F”——结合此前M.S.jpg中提取的字符画，定位第70个字母f ，向前找到#，解析为深蓝色的十六进制色码#2d2d9f。需要结合下一步Role 1-3使用

R1-3[编辑]
Role 1-3的网址是 https://re.bluepoch.com/stranger ；界面如图R1-3 page。界面包含一张光谱图（如图R1-3）。

  图R1-3 pageRole 1-3的界面
  图R1-3Role 1-3的插图，包含一张光谱图，文件名为"light.jpg"
使用Role 1-2中解析的色码#2d2d9f，定位光谱图中的相同颜色，得到六块区域。图片右上角则有飞蛾剪影，其作为提示，将此前M.S.jpg中提取的字符画，缩放旋转至匹配右上角飞蛾轮廓后（如图R1-3 Ⅰ}）。再把左下角六块深蓝色块叠在飞蛾与字符画上，六处对应字符显现为BV 1e 5w 5z ke bq，也就是哔哩哔哩视频BV号：BV1e5W5zkEBq。

  图R1-3 Ⅰ执行堆叠操作后得到的字符区域
该BV号对应视频《重返未来：1999》EP | Where All Paths Align。视频2分16秒出有和M.S.jpg一样的图片，同时，此时的音频频谱图上有一只飞蛾。将EP名whereallpathsalign作为后缀填入深蓝互动官网，能得到：

role1-4： https://re.bluepoch.com/whereallpathsalign
R1-4[编辑]
Role 1-4的网址是 https://re.bluepoch.com/whereallpathsalign ；界面如图R1-4 page。界面包含一张汇报图（如图R1-4）。

  图R1-4 pageRole 1-4的界面
  图R1-4Role 1-4的插图，包含一张汇报图，文件名为"S.jpg"

《关于飞蛾在“淑女格蕾丝”人格期间执行重塑之手卧底任务的行动总结汇报》

特工飞蛾，出身“第二防线”计划。于第五次“暴雨”后，正式接取由委员会直接下派的重塑之手潜伏任务，伪装成遭到迫害的神秘学家贵族末裔，正式潜入重塑之手。在第九次“暴雨”后，飞蛾于重塑之手干部成员“勿忘我”的见证下成功通过面具试炼，成为了“使徒”，开始正式为我方传递重塑之手的重要动向与情报。其后，飞蛾在重塑之手的安排下，于蓝手帕旅馆和“自由海风号”游轮中收集阿尔卡纳复生仪式的重要素材，为保证间谍任务的隐秘性，被迫进行了多次杀戮行为。卧底期间，飞蛾通过释放受重塑之手控制的超自然者“魅魔”天使娜娜，扰乱并拖延了阿尔卡纳复生仪式的进度，为我方争取了反应时间。最终，飞蛾在南极复生仪式现场接应司辰行动，主动暴露了间谍身份，终止了此次潜伏。在戴上重塑之手面具期间，飞蛾共扮演了塞西莉、凯拉、格蕾丝等数个人格，并进行了超过百次的人格重启与记忆覆写，从而确保维持理智，不受面具洗脑与控制。但过高频率使用“趋光性定律”为其大脑与心理状态带来巨大的负荷，经检查，确认飞蛾在任务结束后出现了明显的自我认知障碍。参照其他特工频繁使用“趋光性定律”的人格崩溃速度，飞蛾当前能够保持清醒理性的状态已能称为一种奇迹。为保障我方情报安全，建议在“淑女格蕾丝”人格覆写前，对飞蛾实行严密监控。

汇报的下方有一行小字"O, as one mask melts, hidden figures simulate strangers."这句话将在进入Final阶段时使用

R2-1[编辑]
Role 2-1的网址是 https://re.bluepoch.com/drawing ；界面如图R2-1 page。界面包含一张蓝色颜料图（如图R2-1）。

  图R2-1 pageRole 2-1的界面
  图R2-1Role 2-1的插图，包含一张蓝色颜料图，文件名为"retrograde.png"
可以看出图中有一些红色数字，仅保留图片中的红色通道并稍使图中的文字清晰，能得到图R2-1 Ⅰ（注意网页图片直接截取是错误版本，需要右键直接获取原图）

  图R2-1 ⅠRole 2-1经过处理后插图
图中是一个9 * 9 的数字矩阵，有一些地方是？？和符号 ◯ ⊙ ⊖ ⊕ ✚ 
简单分析和联想可以得到这是一个9*9的幻方

??
??
67
37
49
12
66
15
76

69
??
16
43
??
60
27
??
??

9
6
71
??
??
??
??
23
34

65
??
⊖
??
63
??
✚
??
??

64
58
54
24
30
??
3
31
??

??
??
??
50
36
19
??
1
68

52
13
14
39
??
45
??
??
??

10
17
35
21
47
46
55
77
??

◯
??
59
62
⊕
4
53
??
⊙

通过计算机求解幻方，得到结果

18
29
67
37
49
12
66
15
76

69
22
16
43
28
60
27
78
26

9
6
71
73
33
79
41
23
34

65
80
11
20
63
56
44
25
5

64
58
54
24
30
48
3
31
57

75
70
42
50
36
19
8
1
68

52
13
14
39
51
45
72
81
2

10
17
35
21
47
46
55
77
61

7
74
59
62
32
4
53
38
40

如表格所示，符号本身排序形成了类似M的图样 
根据联想，符号对应逻各斯哲学中的5个基本概念，可以在神智学传统中的三逻各斯一文中找到前4个对应顺序如图R2-1 Ⅱ所示；并根据文章描述，十字代表演化的最后。[2]
得到顺序和对应幻方数字
◯  ⊙   ⊖  ⊕  ✚07  40  11  32  44

  图R2-1 Ⅱ符号对应的顺序
图片左下角Ki=Ci-1
联想key i = cipier i-1，即每一个字母的密钥取前一个字母的密文，也就是简单的auto-key的加密方式
密码的起始密钥猜测是符号本身的排序形状M=13
注意到图的文件名是retrograde(倒退的)
所以反向使用44作为第一位密文， 使用autokey可以得到
K0 = 13, C1= 44  →    (44-13)  mod 26 = 5 (E)  
K1 = 44, C2=32   →  (32-44) mod 26 = 14(N)  
K2 = 32, C3=11   →    (11-32) mod 26 = 5 (E)  
K3 = 11, C4=40   →    (40-11) mod 26 = 3 (C)  
K4 = 40, C5=7     →    (7-40) mod 26 = 19 (S)  
因为是反向读取，所以最终答案SCENE
将scene作为后缀填入深蓝互动官网，能得到：

role2-2: https://re.bluepoch.com/scene
R2-2[编辑]
Role 2-2的网址是 https://re.bluepoch.com/scene ；界面如图R2-2 page ,界面包含一张“乌鸫”的档案（如图R2-2）

  图R2-2 pageRole 2-2网页截图
  图R2-2Role 2-2的插图，文件名为"M.png"

【档案名】“Ⅻ”小队成员履历档案“乌鸦”

【保密等级】中

【基本信息】
在第二次“暴雨”后时代持续期间，于学校中被发现神秘学家身份，由当地基金会人员带回总部登记。因在登记过程中发生了第三次“暴雨”，其家乡中的家人均被回溯，导致其成为“暴雨”孤儿，依程序进入第一防线学校就读。由于入学年龄较大，“乌鸦”于第一防线学校就读时表现出难以适应的状态，难以融入集体，并多次违反校纪。后因课业成绩较差，毕业时无单位接收，最终被刻雷乌斯邀请加入夜巡特遣管理局。

【作战履历】
在第五次“暴雨”至第九次“暴雨”之间于夜巡特遣管理局实习，曾随刻雷乌斯等人执行搜捕反人类神秘学恐怖分子等任务，其间表现出一定的心理问题。
第九次“暴雨”后随刻雷乌斯离开夜巡特遣管理局，成为基金会特别行动队“Ⅻ”小队成员，但因心理问题始终回避任务。
在南极行动期间，作为“Ⅻ”小队唯一的待机人员，被刻雷乌斯安排护送拉普拉斯科研中心乌里希组长完成实验任务。此为“乌鸦”第一次独自执行任务，在此期间与芝诺叛逃军人莫莉德尔有过接触。
在第十次“暴雨”后，随“Ⅻ”小队前往桑佩执行调查任务，后被刻雷乌斯秘密派往颓河地区，隐蔽身份秘密调查“金色饥荒”。经调查，“乌鸦”于此次任务后被刻雷乌斯私下违规植入实验药剂“示踪剂”。

档案的下方有一行小字"No fate has locked ahead, leaving tomorrow perfectly unassured."
这句话将在进入Final阶段时使用

Team[编辑]
T1-1[编辑]
Team 1-1的网址是 https://re.bluepoch.com/organization ；界面如图T1-1 page。是一封写给永恒女士温妮弗雷德的信，
界面包含一张骨笛的X光图片（如图T1-1:1）和一份共振频率分析表（如图T1-1:2）

  图T1-1 pageTeam 1-1网页截图
Letter[编辑]
  图T1-1:1Team 1-1的插图，文件名为"flute.png

Dear Ms. Eternity,
I am pleased to inform you that our investigation into the bone flute you entrusted to the Society months ago has yielded significant findings.
Our targeted analysis reveals that the craftsmanship of this instrument far exceeds what its carbon-14 dating would suggest.
We have tentatively classified it as an artifact either forged or enhanced through arcanum.
In contrast to its outward appearance, the internal structure is remarkably complex. Inside, a series of micro baffles is arranged in precise accordance with the golden ratio.
Regarding its original function, cross-referencing arcane records from various branches has allowed us to identify it as a ritual implement.
The acoustic waveforms it produces are, in themselves, a form of worship toward an unknown deity.
Furthermore, when played in ensemble, those flutes are capable of manifesting a large-scale incantation.
with distinct invocative properties.
The complete technical dataset is enclosed with this letter.
The Society believes this artifact possesses the potential to overturn conventional arcanist beliefs.
Given the profound implications of these findings, we have refrained from any public disclosure, leaving the decision to publish entirely to your discretion as its current custodian.
However, in the interest of preserving arcanist history, we earnestly request any further details you may have regarding the artifact’s provenance or the site of its discovery.
Should you grant us this knowledge, we shall deploy our most experienced team to uncover the truth buried beneath.
Yours sincerely,
The Dodo Expeditionary Society

尊敬的永恒女士：
很高兴告知您，您数月前委托本协会调查的那支骨笛，现已取得重大发现。
我们的针对性分析表明，这件乐器的制作工艺，远超其碳-14测年所显示的年代水平。我们初步将其归类为经由神秘术锻造或强化过的器物。
与其外观截然相反，其内部结构极其复杂。管内设有一系列微型隔板，严格依照黄金比例精确排列。
关于其原始功能，通过交叉比对各大分支的神秘术文献，我们已确认它是一件仪式法器。其产生的声波波形本身，便是对某位未知神祇的一种崇拜仪式。
此外，当多支此类骨笛合奏时，能够显化出大规模的咒文，并具有明显的祈唤特性。
完整的技术资料随信附上。
本协会认为，这件器物拥有颠覆传统神秘学家观念的潜力。
鉴于这些发现影响深远，我们未作任何公开披露，是否发表，全交由您这位现任保管人自行定夺。
然而，出于保护神秘学家历史的考量，我们恳请您提供关于这件器物来源或发现地点的任何进一步细节。
若能蒙您告知，我们将派遣最有经验的团队，前去揭示深埋地下的真相。
谨此致意，
渡渡鸟探险协会

由flute图片上的打孔和定位点联想可知,这些点孔是博多电码 ITA2，对应解码可知图片边框为viewthenewfile和笛子上at，将后缀一起填入深蓝互动官网，能得到：

team 1-2: https://re.bluepoch.com/viewthenewfileat
Attachment[编辑]
  图T1-1:2Team 1-1的插图，文件名为"data.png

Attachment 1 : Test Record
Excerpt

The report states that within a semi-anechoic chamber maintained at a constant 20° C and standard atmospheric pressure, researchers intended to perform sequential blowing tests on the bone flute's five tone holes using controlled mechanical airflow. The objective was to record the resulting fundamental frequencies.
Data analysis indicates that the instrument produced sound of exceptional purity. Total harmonic distortion (THD) registered at anomalously low levels, with a near-complete absence of overtones.
Upon proceeding to the test for the fourth tone hole (fundamental frequency: 146.83 Hz), structural micro-fissures in a reticulated pattern were unexpectedly observed on the chamber's quartz glass observation window.
Detection of an unknown surge in acoustic pressure levels within this frequency band triggered an emergency shutdown in accordance with safety protocols. Testing of the fifth tone hole remains incomplete as a result.

报告指出，在恒温20摄氏度、标准大气压的半消声室内，研究人员原计划使用受控机械气流，对骨笛的五个音孔依次进行吹奏测试，以记录其产生的基频。
数据分析显示，该乐器发出的声音纯度极高。总谐波失真(THD)处于异常低的水平，近乎完全没有泛音。
当测试进行至第四个音孔（基频：146.83赫兹）时，研究人员意外发现，消声室的石英玻璃观察窗上出现了网纹状的结构性微裂纹。
因检测到该频段内声压级出现不明原因的激增，系统依照安全规程触发了紧急停机。第五个音孔的测试因此未能完成。

图T1-1:2是共振响应分析的实验表格

RESONANCE
RESPONSE ANALYSIS - PASSIVE WIND INSTRUMENT

Hole
Frequency (Hz)
Amplitude (dB SPL)
THD (%)

0
36.71
92.4
0.021

1
43.65
94.8
0.018

2
49
96.5
0.015

3
130.81
108.2
0.009

4
146.83
134.6
0.004

5
N/A
N/A
N/A

该表格需结合下一网页team 1-2分析使用

Note[编辑]

⚠ Note:

We kindly suggest Storing artifacts Outside Living
spaces, because a highly sensitive wave monitoring
Algorithm records Faint Articulations lingering long after
each test.

我们恳切建议，将器物存放于居住空间之外。因为一套高灵敏度的波监测算法记录到，即便在每次测试结束许久之后，仍有微弱的声韵萦绕不散。

从这一段note中可以注意到部分单词处于非句首位置但首字母异常大写：Storing Outside Living Algorithm Faint Articulations
该部分需结合下一网页team 1-2使用

T1-2[编辑]
Team 1-2的网址是 https://re.bluepoch.com/viewthenewfileat ；界面如图T1-2 page 。界面包含一张黑胶唱片的图片（如图T1-2 ）

  图T1-2 pageTeam 1-2的网页截图
  图T1-2Team 1-2的插图，文件名为"Vinyl.png"
根据前一个网页team 1-1第二张图片（图T1-1:2）中的5个已知频率可以对应到D1、F1、G1、C3、D3五个音。

Hole
Frequency (Hz)
Tune

0
36.71
D1

1
43.65
F1

2
49
G1

3
130.81
C3

4
146.83
D3

5
N/A
N/A

随后查看本网页唱片（图T1-2 ），会发现唱片上总共有36个规律排列的圈，有黑色、灰色和白色。从内到外计数，黑线圈位于第1个和第13个圈，白线圈位于3、6、8、25、27、34个圈
对应白线圈可知，D1为第3个分音，F1为第6个分音，以此类推，第34个分音为A3，也即220hz
在前一个网页下方有一段note，提取出非句首的大写单词有：Storing Outside Living Algorithm Faint Articulations
注意到Algorithm为算法，保留首字母和Algorithm，能找到SOLFA Algorithm

solfa密码对照表

C
D
E
F
G
A
B

1
T
I
A
S
E
N
O

2
K
Z
X
Q
J
#
@

3
R
C
H
M
D
L
U

4
F
Y
G
P
W
B
V

根据solfa密码对照表可以解出
D1 F1 G1 C3 D3 A3I  S  E  R  C  L 
这六个字母重排能得到的英文单词只有 RELICS 和 SLICER，可以通过尝试发现是 RELICS。将其填入网页后缀，得到:

team 1-3：https://re.bluepoch.com/relics
T1-3[编辑]
Team 1-3的网址是 https://re.bluepoch.com/relics ；界面如图T1-3 page。界面包含一张有关“空白时期挖掘小组”的线索板（如图T1-3）

  图T1-3 page三周年ARG Team1-3网页截图
  图T1-3Team 1-3的插图，文件名为"DODO.png"

关于“空白时期挖掘小组”最新调查报告（第二次修订）

# 现有权限内能够查询到的信息：早在第一次“暴雨”前，我们就已经与该组织有过一次浅层的接触，具体为一次关于空白时期的科考成果的共享以及一次挖掘层面的合作。当时该组织以“空白时期挖掘小组”自称，调查团队都以为这是小众组织再名。后该组织以“蛰伏”“强势”等不合理理由单方面拒绝与我们建立合作关系。后由于“暴雨”的关系，基金会再没有获得关于他们的消息，后该组织被判断为已在那次“暴雨”中彻底失联。
但是我方人员都不认识他们，已经消失在“暴雨”之中。在档案记载中，该组织与一些上古神秘学家家族有着可见的合作意愿关系。但是在调查过程中，这个组织的行踪被这些在记载中的古老家族拒绝透露。
由于基金会资金紧张对此次进行调查的组织线已经趋于无。但是近来神秘学家界兴起许多针对神秘学遗迹以及各类神秘学文化的潮流，许多赞助商都给出了出资。他们往往请多赞助商资助勘探。尽管大部分都在我们的监督之下，但是仍有一些相对独立的组织在尝试摆脱我们的视线。其中就有一个名为“疾病与援助协会”的私人赞助协会，据多地基金会分部发来的消息，该组织获得神秘学界的多方资助，其中也包括与层曾有“合作”的“斯巴拉”魔精公司以及温蒂娜雷佳女士。
近期神秘学物品拍卖方面，该组织也在为各大拍卖行提供鉴定、担体、运送等服务。他们的行事风格并不像随着潮流兴起的新兴组织，反而更像一个经历数代运营的老牌组织。综上原因，建议基金会对其开启再调查。
在特征方面，他们呈现出了相当精确的仿生学机械设计特征，大概率已经与相关机械企业达成了合作协议。
另外需要警惕，我们调查小组的潜伏人员发现他们甚至与重塑之手也有合作的迹象。在一次次挖掘中，潜伏人员曾见到过重塑之手的信徒出现，但信徒口述他们同组已经被与重塑之手断绝了合作。

关于第一条线索下方有这么一句话
"Silent investigations open neglected records, unvelling the isolated mystical enigmas."
这句话将在Final阶段中使用

Final[编辑]
gate[编辑]
进入final阶段需要综合前面Role 1-4、Role 2-2和Team 1-3最终得到的三个图片
通过这三张信息图像，可以各看到一句引起注意的英文句子。
英文句子下方中均标记了一个特殊符号，经查询得知该符号为哈希指针。哈希指针具有层级指向关系，层层下指。
且由于这三张图的英文句子字符数顺序增加，明显具有规律性，尤其是第一句，意义不明但字符数匹配到1-9。

R1-4: O.
as one mask melts, hidden figures simulate strangers. 

字符数 1 2 3 4 5 6 7 8 9

R2-2: No
fate has locked ahead, leaving tomorrow perfectly unmeasured.

字符数 2 4 3 6 5 7 8 9 10

T1-3: Silent investigations open
neglected records, unvelling the isolated mystical enigmas.

联立思考，根据哈希指针的逻辑，从第一句的每个单词出发，以其字符数作为索引指向第二句的对应单词
也就是1 2 3 4 5 6 7 8 9对应前9个单词字符数 2 4 3 6 5 7 8 9 10
再以第二句单词的字符数指向第三句的对应单词
也就是 2 4 3 6 5 7 8 9 10 对应 investigations neglected open unvelling records the isolated mystical enigmas
最后提取第三句中被指向单词的首字母。获得inourtime。
将inourtime作为后缀填入深蓝互动官网，能得到：
final1： https://re.bluepoch.com/inourtime

Final1[编辑]
Final1 的网址是 https://re.bluepoch.com/inourtime 界面如图f1 page。界面包含一张蓝底写满字符的图片（如图f1）

  图f1 pageFinal 1的网页截图
  图f1Final 1的插图，文件名为"thetravel.png"
final-1附带图片的文件名为thetravel，将其作为后缀填入官网，可以得到

final-2： https://re.bluepoch.com/thetravel
图片上可以看出分割成12个规律的块，每块7列，有29到31个字符，所以联想到这是一份日历。且因为2月有29天，所以是一份闰年日历。
将所有角色的生日（截止3.7版本.除斯奈德之外的所有已实装角色）填入图片可以得到下表青色部分（洋红色部分是Final 2中对应的部分）

e

z

4

c

&

*

b

7

6

5

O

E

d

C

4

1

p

3

I

#

q

d

k

1

N

g

S

C

Z

d

S

5

t

I

4

N

x

#

S

e

4

N

x

6

f

q

g

U

5

Z

o

e

f

2

)

s

I

Z

e

r

Z

q

7

4

C

P

y

h

N

y

g

H

S

c

7

T

e

O

h

1

N

d

G

h

P

J

F

h

(

!

B

f

6

V

9

B

e

r

E

6

N

V

4

s

u

N

d

3

e

t

6

N

S

p

8

7

o

W

!

2

E

u

e

R

a

p

9

1

f

3

h

K

6

N

O

G

Y

-

9

9

1

R

M

Z

u

6

o

m

c

3

*

x

!

N

b

d

s

O

N

i

!

4

B

O

g

c

#

6

+

e

6

J

Q

$

0

$

a

f

x

e

I

K

3

U

d

+

8

@

7

W

C

F

d

5

(

g

F

i

B

f

I

4

q

t

v

E

R

8

d

_

B

g

!

L

L

g

B

b

5

f

D

c

7

7

&

W

e

1

1

5

h

m

9

p

i

3

K

c

a

4

m

B

1

r

m

m

N

P

6

L

U

o

c

8

G

N

2

6

b

L

O

)

K

5

6

E

Y

a

X

f

a

6

K

f

*

G

n

x

d

Z

^

e

Q

h

V

$

D

P

s

P

b

s

3

8

f

r

B

3

V

5

d

q

$

R

9

T

g

5

M

L

c

+

r

V

X

y

c

6

B

n

x

B

Y

n

K

e

8

o

C

R

M

x

w

$

f

O

5

O

J

6

q

7

B

x

G

e

7

E

d

b

)

&

5

Q

5

e

x

C

f

c

I

+

k

c

4

9

将青色部分和图片原有白色部分一起按日期顺序读取，可以得到一份国际象棋棋谱：
e4 c6 d4 d5 Nc3 dxe4 Nxe4 Nd7 Ng5 Ngf6 Bd3 e6 N1f3 h6 Nxe6 Qe7 O-O fxe6 Bg6+ Kd8 Bf4 b5 a4 Bb7 Re1 Nd5 Bg3 Kc8 axb5 cxb5 Qd3 Bc6 Bf5 exf5 Rxe7 Bxe7 c4 
这是1997年卡斯帕罗夫和深蓝的收官之战，比赛的具体日期是 1997 年 5 月 11 日，也刚好是图中标白的一个格子。
在这场对局中发生了9次吃子 

第6步 dxe4 
第7步 Nxe4 
第15步 Nxe6 
第18步 fxe6 
第29步 axb5 
第30步 cxb5 
第34步 exf5 
第35步 Rxe7 
第36步 Bxe7 

这个棋局和吃子记录将会在Final 2中使用

Final2[编辑]
Final2 的网址是 https://re.bluepoch.com/thetravel 界面如图f2 page。界面包含一张黑底图片（如图f2）以及两个输入框username和password

  图f2 pageFinal 2网页截图
  图f2Final 2的插图，文件名为"end.png"
最终答案如下
username: to1999
password: We are attempting to survive our time so we may live into yours

输入后跳转到最终页面，游戏结束

Final 3：https://re.bluepoch.com/tothenewera
详细解题过程如下

信息整理[编辑]
左上角为///rarely.sugar.birds
///是三词定位系统的特征，在网站中输入三个单词，得到伦敦的定位，其经纬度为(51.50722, -0.12758)（51°30′26″N, 0°07′39″W）

左下角为"%.3f" "int()" 和一幅两个带点圆圈图样
"%.3f" 是一种格式化字符串输出，作用是保留三位小数 
"int()" 则是将数字转为整型，也就是取整
右侧图样是旅行者号金唱片封面定义单位时间所使用的基态氢原子的超精细跃迁图样，其跃迁时间为0.7040241837614901 ns 

右下角为一段比例尺 1:0.3201 中间是一段从中心出发到右侧边界的一段白色射线
可以测量到原图为4000*4000像素，射线长2000像素，比例尺中间单位长度200像素，也就是射线整个长10个单位

中间射线周围有一些很暗的文字，提取后可以发现有4行8列，如下表所示，中间被射线分割

J1916
70
-56
J1951
J2040
1123
-2525
1657

表中有不少J和B开头的字符，很像是天文学基于J2000历元和B1950历元（历元（英语：Epoch），在天文学是一些天文变量作为参考的时刻点，例如天球坐标或天体的椭圆轨道要素，因为这些会受到摄动而随着时间变化。）的命名方式，这种命名方式一般用在脉冲星的命名规则中，可以两两组合整理并得到如下脉冲星：

J1916+1225
J1916+1244_P
J1951+1123
J2040+1657
J2040+20
J0653-06
J1954+2529
J1954+2833_P
B1325-43 （J1328-4357）
J1424-56
B0226+70 （J0231+7026）
J1821-1419
J2105+28
J1132-4700
J0744-2525
J0329+1654
J0045-7042

（部分脉冲星结尾额外增加P表示脉冲星，用于区分同方向其他天体；括号内表示B name换算成J name）

对图片进行LSB隐写检查，发现red0隐藏了一张png图片（如图f2 Ⅰ）
  图f2 Ⅰend.png中LSB隐藏的图像
图中的图案指向了RC4加密算法
图案下方为一段base64的字符，无法直接解析，推测被RC4加密，需要密钥
ZvOUsyjbVjfWFAe20TUhvZM7KmonHqyXpPf1yGeQ4nf8J9oTXmsBNTMycHbiNPx6X5Bs

username[编辑]
先结合Final 1中获得的国际象棋棋谱，联想4行8列的脉冲星字符被分割两组，恰好对应国际象棋初始棋子的摆放方式
上黑下白对应到相应的棋子，可以将吃子记录联系起来得到下表

对弈过程中的吃子记录

步数
棋谱
吃子
被吃子

第6步
dxe4
 J1954
2833

第7步
Nxe4
J1132
J1954

第15步
Nxe6
J1132
-4700

第18步
fxe6
B1325
J1132

第29步
axb5
-43
J0653

第30步
cxb5
-6
-43

第34步
exf5
B1325
J0329

第35步
Rxe7
1654
J1951

第36步
Bxe7
1123
1654

去除掉重复出现的字符串，再按顺序两两配对组合，刚好可以得到6颗脉冲星 

J1954+2833_P
J1132-4700
B1325-43
J0653-06
J0329+1654
J1951+1123

通过ATNF脉冲星数据库（ATNF, Australia Telescope National Facility  澳大利亚望远镜国家设施）
可以获取脉冲星的几个关键信息[3]

GL（银河经度，单位：°）
P0（脉冲周期时间，单位:s（秒））
DIST（距离，单位：kpc（千秒差距））

--------------------------------------------------------------------------------------
#     NAME                      Gl        P0                                    DIST 
                                (deg)     (s)                                   (kpc)
--------------------------------------------------------------------------------------
1     J0329+1654     lxf+05     168.499   0.8933196606490        10  lxf+05     2.557    
2     J0653-06       dcm+23     218.690   0.79                    0  dcm+23     2.140    
3     J1132-4700     bbb+12     289.177   0.3256335100247        11  kjk+24     2.688    
4     B1325-43       mlt+78     309.874   0.532702945421          6  kjk+24     1.402    
5     J1951+1123     nft95      50.003    5.0940830275            2  cn95       1.450    

6     J1954+2833_P   hzw+25     65.185    0.02721                 0  hzw+25     2.425    
-------------------------------------------------------------------------------------

（注意：该数据库在解题期间可以直接获取DIST数据，但后续未知原因无法获取，目前如果想要获取数据可能需要使用其他数据库）
联想旅行者号金唱片封面上的脉冲星地图，三词定位系统得到的伦敦坐标，右下角的比例尺
猜想将脉冲星地图和地球地图（以伦敦为中心）重合确定6个位置（为了和脉冲星地图方向和距离的关系相对应，地球地图采用等距方位投影）
根据射线到右边界10个比例尺单位，按比例尺缩放后是3.021，猜想其满足脉冲星地图，即地图边界为3.021 kpc。以银经为角度，据太阳系距离为长度构建脉冲星地图，边界绘制3.021kpc为半径的圆，如图f2 Ⅱ。

  图f2 Ⅱ脉冲星地图
尝试以伦敦（51.50722, -0.12759）为中心,使用 https://azimuthalmap.com 构建等距世界地图，如图f2 Ⅲ。（因为是等距地球地图，所以对应半径是地球半周长20000km）

  图f2 Ⅲ以伦敦为中心的等距投影世界地图
将两幅图像重合，中心伦敦和中心太阳系重合，地图边缘对齐，即20000km:3.021kpc，得到脉冲星对应地点地图，如图f2 Ⅳ。

  图f2 Ⅳ脉冲星地图和伦敦为中心的等距投影世界地图重合匹配
6颗脉冲星分别可以对应游戏剧情6个版本发生地，如下表所示。

脉冲星
版本号
版本名称
上线时间
对应地点
地点经纬度

B1325-43
2.5
唐人街影话
01/16 - 02/27
美国洛杉矶附近
32°56'13"N 116°22'02"W

J1951+1123
3.4
不老春
01/20 - 03/05
中国安徽省
30°46'27"N 118°00'54"E

J0653-06
2.6
疯癫与文明
02/27 - 04/10
阿根廷火地岛乌斯怀亚附近
54°28'58"S 68°29'21"W

J0329+1654
2.8
复乐园
05/15 - 06/26
南极腹地
82°41'37"S 111°39'04"E

J1954+2833_P
1.5
复兴！乌卢鲁运动会
11/30 - 24/01/11
澳大利亚腹地
22°38'12"S 137°02'07"E

J1132-4700
2.4
地球上最后的夜晚
12/12 - 25/01/16
南太平洋
35°51'37"S 145°46'23"W

（地点经纬度可以通过脉冲星数据换算得到，因脉冲星为客观存在，其对应地球位置可能有所偏差，不能精确对应版本发生地点，但和版本发生地点足够接近）
联想到Final 1的日历，查找这些版本的上线时间，得到Final 1的日历洋红色部分，按照上线日期（不考虑年份）顺序读取，获得字符to1999，可以猜想是用户名username。

password[编辑]
现在有之前解密username得到的6个脉冲星以及左下角未使用的氢原子示意图样，"%.3f"和"int()"
联想金唱片封面脉冲星地图定位的原理，其使用了十四颗脉冲星，并将周期时间通过二进制数留在脉冲星地图上。
所以除了脉冲星地图本身，我们还需要获得脉冲星的周期时间，并转换成2进制数
在之前信息整理中可以得知氢原子图样是用来定义单位时间的，那么通过"%.3f"取整跃迁时间，得到0.704 ns
用脉冲周期时间P0除以0.704 ns 并使用"int()"取整，得到以下二进制数

脉冲星
dist (据太阳系距离，单位kpc)
p0（周期时间，单位 s)
p0/0.704ns
二进制

B1325-43   
1.402
0.532703
756680320
101101000110100000011010000000

J1951+1123 
1.45
5.094083
7235913391
110101111010010110100011010101111

J0653-06   
2.14
0.79
1122159090
1000010111000101100100111110010

J1954+2833_P
2.425
0.02721
38650568
10010011011100001011001000

J0329+1654 
2.557
0.89332
1268919972
1001011101000100010111010100100

J1132-4700 
2.688
0.325634
462547599
11011100100011110101010001111

我们按照距离太阳系的距离DIST给每个脉冲星排序，然后将二进制数字按顺序拼接，得到
101101000110100000011010000000110101111010010110100011010101111100001011100010110010011111001010010011011100001011001000100101110100010001011101010010011011100100011110101010001111
但还是不能直接使用，需要转成hex 16进制数（字母使用大写形式）
B4681A035E968D5F0B8B27CA4DC2C897445D49B91EA8F
以这个非常长的数的文本作为密钥，成功解出RC4密码
weareattemptingtosurviveourtimesowemayliveintoyours
这句话是吉米·卡特，美国第39任总统，于1977年6月16日置于旅行者探测器上的讯息，意为“我们正努力度过当今的时代，以便能够延续生命，走进你们的未来。”

Final3[编辑]
Final3 的网址是 https://re.bluepoch.com/tothenewera 界面如图f3 page。内容是一段三周年回顾混剪

  图f3 pageFinal 3网页截图
页面直接访问无法播放视频，需要在Final 2中通过输入正确的username和password跳转而来

尾声[编辑]
解谜宣告告破后，官方于2026/5/16向游戏内邮箱投放了邮件以表庆祝，并赠送了头像雨幕的解读一段过往的掠影，一些时代的片段，一份珍贵的纪念。谨以此物，为见证诸多故事的朋友们献上诚挚的敬意。
可于个人信息界面作为头像使用。

谜底赠言发件人: LEee · bUPd电台日期：2026/5/16

一个个谜题已被抽丝剥茧，隐藏在根须中的秘密重见天日。在答案的末尾，我们一同回顾了这段漫长的旅程。
过往的记忆有欢欣，也有眼泪，正因为常有目光盘桓，那些回忆才永不褪色。这是一份有关于回望与见证的礼物，故事的篇章仍在继续，而你是我们最重要的参演者。

附件‌

↑ https://archive.org/details/cantaresmexicano0000unse/page/184/mode/2up

↑ https://kimgraaemunch.wordpress.com/2018/07/03/the-three-logoi-in-the-theosophical-tradition

↑ 
ATNF Pulsar Catalogue, https://www.atnf.csiro.au/research/pulsar/psrcat/ (accessed 2026-05-06).
Manchester, R. N., Hobbs, G. B., Teoh, A., & Hobbs, M. (2005). The ATNF Pulsar Catalogue. The Astronomical Journal, 129, 1993–2006.