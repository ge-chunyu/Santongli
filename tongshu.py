from constants import ganzhi, jieqi, xiudu, xingxiu
from fractions import Fraction
import pandas as pd
from suishu import tuiSui, tuiTaisui

# %% 統術

# 推日月元統，置太極上元以來，外所求年，盈元法除之，餘不盈統者，則天統甲子以來年數也。盈統，除之，餘則地統甲辰以來年數也。又盈統，除之，餘則人統甲申以來年數也。各以其統首日為紀。


def tuiYuantong(x):
    """
    推元統：求距上元年數在哪統那年
    統母：元法、統法
    Args:
        x: 距上元年數
    Returns:
        dict: 統, 統首日干支, 統首日干支序數, 入統年
    """
    santong = ["天統甲子", "地統甲辰", "人統甲申"]
    tongshu = x % 4617 // 1539
    rutongnian = x % 4617 % 1539
    return {"tong": santong[tongshu],
            "tongshouri": santong[tongshu][-2:],
            "t": ganzhi.index(santong[tongshu][-2:]),
            "n": rutongnian}

#  推天正，以章月乘人[入]統歲數，盈章歲得一，名曰積月，不盈者名曰閏餘。閏餘十二以上，歲有閏。求地正，加積月一；求人正，加二。


def tuiTianzheng(x):
    """
    推天正：求 x 年有沒有閏月
    統母：章月、章歲
    入統年：推元統
    Returns:
    tuple: 積月，閏餘，閏餘大於 12，有閏月
    """
    tong = tuiYuantong(x)
    jiyue = tong["n"] * 235 // 19         # 積月
    runyu = tong["n"] * 235 % 19          # 閏餘
    return jiyue, runyu

# 推正月朔，以月法乘積月，盈日法得一，名曰積日，不盈者名曰小餘。小餘三十八以上，其月大。積日盈六十，除之，不盈者名曰大餘。數從統首日起，算外，則朔日也。\
# 求其次月，加大餘二十九，小餘四十三。小餘盈日法得一，從大餘，數除如法。求弦，加大餘七，小餘三十一。求望，倍弦。


def tuiZhengyueshuo(x):
    """
    推正月朔：求 x 年的積日、積日小餘、朔日干支
    統母：月法、日法
    積月：推天正
    Returns:
    dict: 積日，積日大餘，小餘，朔日干支
    """
    tong = tuiYuantong(x)
    j, r = tuiTianzheng(x)
    jiri = (j * 2392) // 81
    dayu = jiri % 60
    jirixiaoyu = (j * 2392) % 81
    # 本年朔旦干支
    shuoriGanzhi = ganzhi[(
        tong['t'] + jiri) % 60]
    return {"jiri": jiri,
            "jiridayu": dayu,
            "jirixiaoyu": jirixiaoyu,
            "shuori": shuoriGanzhi}

# 推閏餘所在，以十二乘閏餘，加(十)[七]得一。盈章中，數所得，起冬至，算外，則中至終閏盈。中氣在朔若二日，則前月閏也。


def tuiRunyu(x):
    """
    推閏餘：求閏月在哪月
    統母：章中
    推天正: 閏餘
    Returns:
    月數 as an int：平年 12，閏年 13
    本年月名 as a list
    """
    j, r = tuiTianzheng(x)
    runyue = (228 - 12 * r)//7 + 1
    if r < 12:
        nm = 12
        m = [str(i) + "月" for i in range(1, 13)]
    else:
        nm = 13
        m = list(range(1, 14))
        m = [str(i) + "月" if i < runyue+1 else str(i-1) + "月" for i in m]
        try:
            m[runyue] = "閏" + str(runyue) + "月"
        except IndexError:
            m[-1] = "閏" + str(runyue-1) + "月"
    return nm, m, runyue


def tuiShuowang(x):
    """
    推朔望弦日：求 x 年自天正月朔日起的朔日、上弦日、望日干支
    Returns:
    朔日、上弦日、望日、下弦日干支，大餘、小餘
    """
    tong = tuiYuantong(x)
    t = tong['t']
    j, r = tuiTianzheng(x)
    nm, m, runyue = tuiRunyu(x)
    jiri = (j * 2392) // 81
    xy = (j * 2392) % 81
    dy = jiri % 60
    sr = [qiuRiming(dy, xy, 29, 43, 81, i, t) for i in range(nm)]
    sx = [qiuRiming(dy, xy, 7, 31, 81, 4*i+1, t) for i in range(nm)]
    w = [qiuRiming(dy, xy, 14, 62, 81, 2*i+1, t) for i in range(nm)]
    xx = [qiuRiming(dy, xy, 7, 31, 81, 4*i+3, t) for i in range(nm)]
    m = [i + "大" if j + 43 >= 81 else i +
         "小" for i, j in zip(m, [p[2] for p in sr])]
    riming = {
        "月": m,
        "朔日": [i[0] for i in sr],
        "上弦": [i[0] for i in sx],
        "望日": [i[0] for i in w],
        "下弦": [i[0] for i in xx],
        "朔日大餘": [i[1] for i in sr],
        "上弦大餘": [i[1] for i in sx],
        "望日大餘": [i[1] for i in w],
        "下弦大餘": [i[1] for i in xx],
        "朔日小餘": [i[2] for i in sr],
        "上弦小餘": [i[2] for i in sx],
        "望日小餘": [i[2] for i in w],
        "下弦小餘": [i[2] for i in xx]
    }
    return pd.DataFrame(riming)

# %%


def qiuRiming(dy, xy, dyc, xyc, fa, i, t):
    """
    求日名：給定大餘、小餘、大餘差、小餘差與法，計算一系列日子的日名
    Args:
    dy: 大餘
    xy: 小餘
    dyc: 大餘差
    xyc: 小餘差
    fa: 法，即小餘的分母
    i: 大餘差對應的距離
    Returns:
    日名、次大餘、次小餘
    """
    cidayu = (t + dy +
              dyc * i + (xy + xyc * i) // fa) % 60
    cixiaoyu = (xy + xyc * i) % fa
    riming = ganzhi[cidayu]
    return [riming, cidayu, cixiaoyu]


# 推冬至，以(算)[策]餘乘(人)[入]統歲數，盈統法得一，名曰大餘，不盈者名曰小餘。除數如法，則所求冬至日也。\
# 求八節，加大餘四十五，小餘千一百。求二十四氣，三其小餘，加大餘十五，小餘千一十。\
# 推中部二十四氣，皆以元為法。


def tuiDongzhi(x):
    """
    推冬至：求 x 年的冬至大餘、小餘、干支
    統母：策餘、統法
    Returns:
    冬至干支、大餘、小餘
    """
    t = tuiYuantong(x)
    dongzhiDayu = t['n'] * 8080 // 1539 % 60
    dongzhiXiaoyu = t['n'] * 8080 % 1539
    dongzhiXushu = t['n'] * 8080 // 1539 % 60
    dongzhiGanzhi = ganzhi[(
        t['t'] + dongzhiXushu) % 60]
    return {"dongzhi": dongzhiGanzhi,
            "dongzhiDayu": dongzhiDayu,
            "dongzhiXiaoyu": dongzhiXiaoyu}


def tuiJieqi(x):
    t = tuiYuantong(x)
    dzDayu = t['n'] * 8080 // 1539 % 60
    dzXiaoyu = t['n'] * 8080 % 1539
    jq = [["節氣", "干支", "大餘", "小餘"]]
    jq.append([jieqi[0], ganzhi[(
        t['t'] + dzDayu) % 60],
        dzDayu, dzXiaoyu])
    for i in range(1, 24):
        jq.append([jieqi[i]] + qiuRiming(dzDayu, dzXiaoyu *
                  3, 15, 1010, 4617, i, t['t']))
    return jq

# 推合晨所在星，置積日，以統法乘之，以十九乘小餘而并之。盈周天，除去之；不盈者，令盈統法得一度。數起牽牛，算外，則合晨所入星度也。


def tuiHechen(x):
    """
    推合晨：以積日、積日小餘求合晨所在星度
    統母：統法、周天、章歲
    積日、小餘：推正月朔
    Returns:
    tuple: 合晨度、合晨度小餘
    """
    shuori = tuiZhengyueshuo(x)
    hechendu = (shuori['jiri'] * 1539 +
                shuori['jirixiaoyu'] * 19) % 562120 // 1539
    hechenXiaoyu = (shuori['jiri'] * 1539 +
                    shuori['jirixiaoyu'] * 19) % 562120 % 1539
    return hechendu, hechenXiaoyu

# 推其日夜半所在星，以章歲乘月小餘，以減合晨度。小餘不足者，破全度。


def tuiRiyeban(x):
    """
    推日夜半所在星：求朔日夜半太陽所在星度
    Args:
    hechendu: 合晨度
    hechenXiaoyu: 合晨度小餘
    xiaoyu: 積日小餘
    Returns:
    tuple: 整數星度，Fraction(分數星度, 1539)
    """
    # 如果合晨度是 0 怎麼辦？
    hc, hcxy = tuiHechen(x)
    sr = tuiZhengyueshuo(x)
    d = (hc * 1539 + hcxy - 19 * sr['jirixiaoyu']) // 1539
    x = (hc * 1539 + hcxy - 19 * sr['jirixiaoyu']) % 1539
    if d < 0:
        d = 365 + d - 1
        x = 1539 - x
    return d, Fraction(x, 1539)

# 推其月夜半所在星，以月周乘月小餘，盈統法得一度，以減合晨度。


def tuiYueyeban(x):
    """
    推月夜半所在星：求朔日夜半月亮所在星度
    Args:
    hechendu: 合晨度
    hechenXiaoyu: 合晨度小餘
    xiaoyu: 積日小餘
    Returns:
    tuple: 整數星度，Fraction(分數星度, 1539)
    """
    hc, hcxy = tuiHechen(x)
    sr = tuiZhengyueshuo(x)
    d = (hc * 1539 + hcxy - 254 * sr['jirixiaoyu']) // 1539
    x = (hc * 1539 + hcxy - 254 * sr['jirixiaoyu']) % 1539
    if d < 0:
        d = 365 + d - 1
        x = 1539 - x
    return d, Fraction(x, 1539)

# 推月食，置會餘歲積月，以二十三乘之，盈百三十五，除之。不盈者，加二十三得一月，盈百三十五，數所得，起其正，算外，則食月也。加時，在望日衝辰。


def tuiYueshi(j):
    """
    推月食：根據距上元年數 n 計算當年有無月食以及月食月份
    Args:
    n: 距上元年數
    Returns:
    """
    # j = ((n % 513) * 235) % 19
    ciyu = (23 * j) % 135
    yueshi = (135 - ciyu) // 23 + 1
    return yueshi

# Convert 合晨度、日月夜半星度 to 星度


def convertXingdu(du):
    """
    convert du into 星宿度數，自牽牛初度起算，牽牛起于 0 度
    Args:
    合晨度、日月度數
    Returns:
    合辰、日月所在星及度數
    """
    xiu = xingxiu[1:] + xingxiu[0:1]
    xd = du + 1
    i = -1
    for i, j in enumerate(
            xiudu[1:] + xiudu[0:1]):
        cd = xd - j
        if cd > 0:
            xd = cd
            i += 1
        else:
            break
    return xiu[i], xd

# 求一年日期


def calCalendar(x):
    """
    推朔望弦日：求入統 n 年自天正月朔日起的朔日、上弦日、望日干支
    Args:
    j: 積月
    runyu: 閏餘
    tongshouri: 統首日干支
    Returns:
    朔日、上弦日、望日干支，大餘、小餘
    """
    t = tuiYuantong(x)
    jiyue, runyu = tuiTianzheng(x)
    nm, m, runyue = tuiRunyu(x)
    sr = tuiZhengyueshuo(x)
    jirixiaoyu = sr['jirixiaoyu']
    jiridayu = sr['jiridayu']
    riqi = {}
    shuo = (t['t'] + jiridayu) % 60
    xy = jirixiaoyu
    for i in range(1, nm+1):
        # if i < runyu
        if xy + 43 >= 81:
            yue = m[i-1] + "大"
        else:
            yue = m[i-1] + "小"
        gz, cidayu, cixiaoyu = qiuRiming(jiridayu, jirixiaoyu,
                                         29, 43, 81, i, t['t'])
        if shuo < cidayu:
            riqi[yue] = [ganzhi[j] for j in range(shuo, cidayu)]
        else:
            riqi[yue] = [ganzhi[j] for j in
                         list(range(shuo, 60)) + list(range(0, cidayu))]
        shuo = cidayu
        xy = cixiaoyu
    riqi = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in riqi.items()]))
    return riqi

# 推距上元 x 年元統、歲次、有無閏月、朔日、冬至、合辰、日月夜半


def calcYear(x):
    """
    求年曆：求距上元任意一年 n 的正月朔、冬至、
    """
    t = tuiYuantong(x)
    sui = tuiSui(x)
    nian = tuiTaisui(x)
    j, r = tuiTianzheng(x)
    sr = tuiZhengyueshuo(x)
    dz = tuiDongzhi(x)
    hc, hcXy = tuiHechen(x)
    rhc, rhcx = tuiRiyeban(x)
    yhc, yhcx = tuiYueyeban(x)
    hcx, d = convertXingdu(hc)
    rx, rd = convertXingdu(rhc)
    yx, yd = convertXingdu(yhc)
    if r >= 12:
        run = "有"
    else:
        run = "無"
    print(f"距上元{x}年入{t['tong']} {t['n']}年\n歲次{sui['ci']}，在{
          sui['xiu']}宿{sui['du']}度，太歲在{nian}")
    print(f"本年積月{j}，閏餘{r}")
    print(f"本年{run}閏月")
    if r >= 12:
        nm, m, runyue = tuiRunyu(x)
        print(f"閏{runyue}月")
    print(f"朔日：{sr['shuori']}, 積日：{sr['jiri']}，大餘：{
          sr['jiridayu']}，小餘：{sr['jirixiaoyu']}")
    print(f"冬至爲{dz['dongzhi']}，大餘{dz['dongzhiDayu']}，小餘{dz['dongzhiXiaoyu']}")
    print(f"合晨度{hc}，合晨小餘{hcXy}, 合辰在{hcx} {d} 度")
    print(f"日夜半{rhc}度，{rhcx}分，日在{rx} {rd} 度")
    print(f"月夜半{yhc}度，{yhcx}分，月在{yx} {yd} 度")
