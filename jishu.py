from constants import (ganzhi,
                       shierci,
                       jieqi, cixiu)
from tongshu import tuiRunyu
# %% 紀術

# 推五星見復，置太極上元以來，盡所求年，乘大統見復數，盈歲數得一，則定見復數也。不盈者名曰見復餘。見復餘盈其見復數，一以上見在往年，倍一以上，又在前往年，不盈者在今年也。


def tuiJianfu(x, planet):
    """
    推五星見復：由距上元年數 x，求五星見復出現年數
    Args:
    紀母：大統見復數 (見中法)、歲數
    x: 距上元年數
    planet: an object with Jimu using 見復數，即見中法 and 歲數
    Returns:
    jianfu: 見復，1 在今年，2 在去年，3 在前年
    jianfuYu: 見復餘
    dingJianfu: 定見復數
    """
    dingJianfu = (x * planet.jianZhongfa) // planet.cycle
    jianfuYu = (x * planet.jianZhongfa) % planet.cycle
    jfd = jianfuYu / planet.jianZhongfa
    if jfd < 1:
        jianfu = 1           # 以距上元年數算，見復在距上元年數年內，如果以此紀年，要將距上元年數減一，見復在本年
    elif 1 <= jfd and jfd < 2:
        jianfu = 2           # 見復在去年
    elif jfd >= 2:
        jianfu = 3           # 見復在前年
    return {"jianfu": jianfu, "jianfuYu": jianfuYu, "dingJianfu": dingJianfu}

# 推星所(一多“在”字)見中次，以見中分乘定見復數，盈見中法得一，則積中法也。不盈者名曰中餘。以元中除積中，餘則中元餘也。以章中除之，餘則入章中數也。以十二除之，餘則星見中次也。中數從冬至起，次數從星紀起，算外，則星所見中次也。


def tuiZhongci(x, planet):
    """
    tuiZhongci: 推星所見中次，以推見復所求的定見復數
    Args:
    定見復數：推見復
    紀母：見中分、見中法
    統母：元中、章中
    Returns:
    積中、中餘、中元餘、星見中次、中氣
    c: 十二次
    q: 中氣
    """
    jianfu = tuiJianfu(x, planet)
    jizhong = jianfu["dingJianfu"] * planet.jianzhongfen // planet.jianZhongfa
    zhongyu = jianfu["dingJianfu"] * planet.jianzhongfen % planet.jianZhongfa
    zhongyuanyu = jizhong % 55404
    zhongci = jizhong % 55404 % 228 % 12
    return {"jizhong": jizhong, "zhongyu": zhongyu,
            "zhongyuanyu": zhongyuanyu,
            "zhongci": zhongci, "ci": shierci[zhongci],
            "zhongqi": jieqi[zhongci * 2]}

#  推星見月，以閏分乘定見，以章歲乘中餘從之，盈見月法得一，并積中，則積月也。不盈者名曰月中餘。以元月除積月餘，名曰月元餘。以章月除月元餘，則入章月數也。以十二除之，至有閏之歲，除十三。入章三歲一閏，六歲二閏，九歲三閏，十一歲四閏，十四歲五閏，十七歲六閏，十九歲七閏。不盈者數起於天正，算外，則星所見月也。


def tuiXingjianyue(x, planet):
    """
    推星見月，以推星所見中次所求得的積中、中餘
    Args:
    定見復數：推見復
    積中、中餘：推星所見中次
    紀母：(見)閏分、見中法、見月法
    統母：元月、章月
    Returns:
    積月、月餘、月元餘、入章月
    """
    jianfu = tuiJianfu(x, planet)
    zhongci = tuiZhongci(x, planet)
    jiyue = (planet.jianRunfen * jianfu["dingJianfu"] + zhongci["zhongyu"] *
             19) // planet.jianYuefa + zhongci["jizhong"]
    yueyu = (planet.jianRunfen * jianfu["dingJianfu"] + zhongci["zhongyu"] *
             19) % planet.jianYuefa
    yueyuanyu = jiyue % 57105
    ruzhangyue = yueyuanyu % 235
    y = ruzhangyue // 12
    m = ruzhangyue % 12 - \
        len([i for i in [3, 6, 9, 11, 14, 17, 19] if y - i > 0]) + 1

    if m <= 0:
        m += 12
    month = tuiRunyu(x-jianfu['jianfu'])[1][m-1]
    return {"jiyue": jiyue, "yueyu": yueyu,
            "yueyuanyu": yueyuanyu,
            "ruzhangyue": ruzhangyue,
            "xingjianyue": month}


# 推至日，以中法乘中元餘，盈元法得一，名曰積日，不盈者名曰小餘。小餘盈二千五百九十七以上，中大。數除積日如法，算外，則冬至也。

def tuiZhiri(x, planet):
    """
    推至日：求星見所在中氣的干支
    Args:
    中元餘，推星所見中次所得
    統母：中法、元法
    Returns:
    積日、小餘、至日干支序數、至日干支
    """
    zhongci = tuiZhongci(x, planet)
    jiri = zhongci["zhongyuanyu"] * 140530 // 4617
    xiaoyu = zhongci["zhongyuanyu"] * 140530 % 4617
    zhiri = jiri % 60
    return {"jiri": jiri, "xiaoyu": xiaoyu,
            "zhiri": zhiri, "zhiriGanzhi": ganzhi[zhiri]}


# 推朔日，以月法乘月元餘，盈日法得一，名曰積日，餘名曰小餘。小餘三十八以上，月大。數除積日如法，算外，則星見月朔日也。


def tuiShuori(x, planet):
    """
    推朔日：求星見之月的朔日
    Args:
    統母：月法、日法
    月元餘，即推星見月所求
    Returns:
    積日、小餘、星見月朔日
    """
    yue = tuiXingjianyue(x, planet)
    jiri = (yue["yueyuanyu"] * 2392) // 81
    jirixiaoyu = (yue["yueyuanyu"] * 2392) % 81
    shuori = jiri % 60
    return {"jiri": jiri, "jirixiaoyu": jirixiaoyu,
            "shuori": ganzhi[shuori]}


# 推入中次日度數，以中法乘中餘，以見中法乘其小餘并之，盈見中日法得一，則入中日入次度數也。中次至日數，次以次初數，算外，則星所見及日所在度數也。求夕，在日後十五度。


def tuiRuzhongci(x, planet):
    """
    推入中次日度數
    Args:
    統母：中法；紀母：見中法、見中日法
    中餘，推星所見中次所求
    小餘，推至日所求
    Returns:
    入中次日度數
    """
    zhongci = tuiZhongci(x, planet)
    zhiri = tuiZhiri(x, planet)
    ruzhong = (zhongci["zhongyu"] * 140530 + zhiri["xiaoyu"]
               * planet.jianZhongfa) // planet.jianZhongRifa + 1
    return ruzhong

# 推入月日數，以月法乘月餘，以見月法乘其小餘并之，盈見月日法得一，則入月日數也。并之大餘，數除如法，則見日也。


def tuiRuyueri(x, planet):
    """
    推入月日：求星見在所在月的日數
    Args:
    統母：月法
    紀母：見月法、見月日法
    月餘：推星見月所得
    積日小餘：推朔日所得
    Returns:
    入月日
    """
    jian = tuiXingjianyue(x, planet)
    shuori = tuiShuori(x, planet)
    ruyueri = (jian["yueyu"] * 2392 + shuori['jirixiaoyu'] *
               planet.jianYuefa) // planet.jianYueRifa + 1
    rigz = ganzhi[(ruyueri + shuori['jiri']) % 60 - 1]
    return ruyueri, rigz


# %%

def convertWuxingdu(c, rz):
    """
    由十二次、入中度數求在本次何宿幾度
    Args:
        c: 十二次序數
        rz: 入中
    Returns:
        宿、度
    """
    d = rz
    xiu = cixiu[shierci[c]]
    for i in range(len(cixiu[shierci[c]])):
        if d - xiu[i][1] > 0:
            d = d - xiu[i][1]
        else:
            break
    if i == 0:
        d += cixiu[shierci[c-1]][-1][1]
    return xiu[i][0], d


def qiuXingjian(x, planet):
    jianfu = tuiJianfu(x, planet)
    zc = tuiZhongci(x, planet)
    jy = tuiXingjianyue(x, planet)
    zr = tuiZhiri(x, planet)
    sr = tuiShuori(x, planet)
    rz = tuiRuzhongci(x, planet)
    ri, rgz = tuiRuyueri(x, planet)
    xiu, du = convertWuxingdu(zc['zhongci'], rz)
    print(f"{planet.name} 始見在{x-jianfu['jianfu']}年\n\
入章月 {jy['ruzhangyue']}\n\
{jy['xingjianyue']}{sr['shuori']}朔{rgz} {ri} 日，\n\
星見在{zc['zhongqi']}{zr['zhiriGanzhi']}後，\n\
在{zc['ci']} {rz} 度，{xiu}宿 {du} 度 ")
