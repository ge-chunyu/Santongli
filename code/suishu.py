from constants import ganzhi, shierci, juXing, chudu, xiudu, xingxiu
# %% 歲數


def tuiSui(n):
    """
    推歲所在：求歲星所在星次
    Args:
    n: 距上元年數
    Returns:
    求歲星所在星次序數，積次，次餘，十二次
    """
    jici = 145 * (n % 1728) // 144
    ci = jici % 12
    ciyu = 145 * (n % 1728) % 144
    jidu = (ciyu * 30) // 144

    cichu, cizhong = juXing[ci:ci+2]
    cijian = xiudu[cichu:cizhong+1]
    cijian[0] -= chudu[ci]
    xiuIn = -1
    for i, j in enumerate(cijian):
        if jidu - j > 0:
            jidu -= j
            xiuIn = i
        else:
            break
    if cichu+xiuIn+1 > 27:
        x = xingxiu[0]
    else:
        x = xingxiu[cichu+xiuIn+1]
    if xiuIn == -1:
        jidu = jidu + chudu[ci]
    return {'jici': jici, 'ci': shierci[ci],
            'xiu': x, 'du': jidu}

# %%


def tuiTaisui(n):
    """
    推太歲：根據積次求本年的干支名
    干支自丙子起
    Args:
    jici: 積次
    Returns:
    年干支
    """
    jici = 145 * (n % 1728) // 144
    tsN = jici % 60
    nian = ganzhi[(12 + tsN) % 60]
    return nian
