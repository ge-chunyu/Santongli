# %%
# from importlib import reload
from jimu import jimu
from constants import ganzhi
import tongshu as ts
import suishu
import jishu as js

# %%
ts.tuiYuantong(-1)

########################################
# %% 求三統八十一章章首朔日干支大小餘
shuori = []
dongzhi = []

for i in range(81 * 3):
    t = ts.tuiYuantong(19 * i)
    shuori.append([t['tong'], i % 81 + 1] +
                  list(ts.tuiZhengyueshuo(i).values()))
    dongzhi.append([t['tong'], i % 81 + 1] + list(ts.tuiDongzhi(i).values()))

for i in range(81):
    print("\t".join([str(i+1), shuori[i][5], shuori[81+i][5],
                     shuori[81*2+i][5]]))

shuori


########################################
# %% 世經
########################################
# 世經所載距上元年數


def tuiNian(x):
    t = ts.tuiYuantong(x)
    j, runyu = ts.tuiTianzheng(x)
    sr = ts.tuiZhengyueshuo(x)
    dz = ts.tuiDongzhi(x)
    jici, ci, xing, du = suishu.tuiSui(x)
    print(x, t['tong'], t['n'], sr['shuori'],
          dz['dongzhi'], ci, xing, du)


# %%
for n in [141480, 142109, 142576, 142577, 143025, 143127]:
    tuiNian(n)

tuiNian(142120)

# 驗算世經載有朔旦冬至干支距上元年數
sui = [141493, 141588, 142121, 142197, 142273,
       142349, 142425, 142501, 142577, 142653,
       142710, 142729, 142805, 142881, 142957,
       143032, 143108, 143127, 143184]
for i in sui:
    if i < 143025 and i > 142109:
        x = i - 1
    else:
        x = i
    t = ts.tuiYuantong(x)
    j, runyu = ts.tuiTianzheng(n)
    shuori = ts.tuiZhengyueshuo(x)
    dz = ts.tuiDongzhi(x)
    print(i, x, t['tong'], t['n'], shuori['shuori'], dz['dongzhi'])

# %% 驗算世經歲次
sui = [141480, 142097, 142109, 142577, 142588, 142596, 142687, 142689, 142690,
       142698, 142700, 142722, 143025, 143127, 143255]
for i in sui:
    if i < 143025 and i > 142109:
        x = i - 1
    else:
        x = i
    print(i, suishu.tuiSui(x))

# %% 驗算世經閏月
sui = [142109, 142606, 142611, 142686, 142710]
for i in sui:
    if i < 143025 and i > 142109:
        x = i - 1
    else:
        x = i
    t, g, n = ts.tuiYuantong(x)
    j, runyu = ts.tuiTianzheng(n)
    if runyu >= 12:
        r = ts.tuiRunyu(runyu)
    else:
        r = 0
    print(i, runyu, r)
suishu.tuiTaisui(403)

# %% 驗算世經日名
# %% 求距上元任意一年某月某日干支日名


def convertDate(x, m, d):
    """
    求距上元任意一年 x, m 月，d 日的干支日名
    """
    if x < 143025 and x > 142109:
        x = x - 1
    else:
        x = x
    t = ts.tuiYuantong(x)
    jiyue, runyu = ts.tuiTianzheng(x)
    sr = ts.tuiZhengyueshuo(x)
    ri, cdy, cxy = ts.qiuRiming(
        sr['jiridayu'], sr['jirixiaoyu'], 29, 43, 81, m-1, t['t'])
    xushu = cdy + d - 1
    ri = ganzhi[xushu % 60]
    return xushu, ri


# %%
ri = [["周公攝政七年", "乙亥", 142123, 2, 1],
      ["周公攝政七年", "庚寅", 142123, 2, 16],
      ["周公攝政七年", "乙未", 142123, 2, 21],
      ["周公攝政七年", "甲辰", 142123, 3, 1],
      ["周公攝政七年", "丙午", 142123, 3, 3],
      ["周公攝政七年", "戊辰", 142123, 13, 29],
      ["成王元年", "己巳", 142124, 1, 1],
      ["成王三十年", "庚戌", 142153, 4, 1],
      ["成王三十年", "甲子", 142153, 4, 15],
      ["成王三十年", "乙丑", 142153, 4, 16],
      ["康王十二年", "戊辰", 142165, 6, 1],
      ["康王十二年", "庚午", 142165, 6, 3],
      ["釐公五年", "甲午", 142577, 8, 18],
      ["釐公五年", "丙子", 142577, 12, 1],
      ["文公十一年", "甲子", 142616, 3, 1],
      ["襄公二十七年", "乙亥", 142686, 9, 1],
      ["襄公三十年", "癸未", 142689, 2, 24],
      ["昭公十八年", "丙子", 142708, 5, 8],
      ["昭公十八年", "戊寅", 142708, 5, 10],
      ["昭公十八年", "壬午", 142708, 5, 14]
      ]

# %%

for i in ri:
    x, d = convertDate(i[2], i[3], i[4])
    print(f"| {i[0]} | {i[1]} | {i[2]} | {i[3]}月{i[4]}日 | {d}")

# %% 康王十二年八月朏
convertDate(142165, 8, 3)

# %%
ts.tuiShuowang(142122)

# %% 求襄公二十七年 142686 朔日干支
ts.tuiShuowang(142685)[['月', '朔日', '朔日大餘', '朔日小餘']]

# %% 求昭公二十年 142710 朔日干支
ts.tuiShuowang(142709)[['月', '朔日', '朔日大餘', '朔日小餘']]

# %% 求襄公二十七年 142686 朔日干支
ts.tuiShuowang(142685)[['月', '朔日', '朔日大餘', '朔日小餘']]

# %% 驗算世經襄公三十年積日

jy = [ts.tuiTianzheng(i) for i in [142615, 142688]]
(jy[1][0] - jy[0][0]-2) * 2392/81 + 53
jy

# 文公十一年到襄公三十年閏年數
len([j for j in [ts.tuiRunyu(i) for i in range(142615, 142689)] if j != 0])
(142688-142615)*12 + 27

# %%
# 驗算日月行度
# 驗算伐紂前一年 142108 殷十一月戊子，即周十二月戊子的日月星度
# 1. 求伐紂之年朔日合晨度，337，小餘 421；日夜半 336 度，小餘 1409；月夜半 332 度，小餘 250
# 2. 上一年殷十一月戊子是三天前，這天夜半日度數爲 333；月兩天行 26 14/29 度，月在 305 1155/1539
# 3. 轉換成星度就是箕 6 度餘 1409/1539
ts.tuiHechen(142109)
ts.tuiRiyeban(142109)
ts.tuiYueyeban(142109)
ts.convertXingdu(337)
ts.convertXingdu(333)               # 伐紂之年朔日合晨度
ts.convertXingdu(305)               # 十一月戊子日夜半星度
ts.tuiZhengyueshuo(142109)          # 十一月戊子月夜半星度

# %%

# 驗算釐公五年十二月 142577 丙子日月行度
# 1. 求釐公六年 142578 正月朔積日：361221
# 2. 減去釐公五年十二月的日數：十二月小丙子朔，29 天，無小餘
# 3. 求釐公五年十二月朔丙子合晨度：（積日 * 統法 + 19 * 小餘）% 周天 // 統法，324
# 4. 求 324 度所在星度，從牽牛初度起算，算外加一
ts.tuiZhengyueshuo(142577)['jiri']
ts.tuiShuowang(142576)[['月', '朔日', '朔日小餘']]
ts.tuiZhengyueshuo(142577)['jiri'] - 29
(361192 * 1539) % 562120 // 1539
ts.convertXingdu(324)

# %% 驗算伐紂之年辰星行度
x = 142109
Mercury = jimu('Mercury')
js.tuiJianfu(x, Mercury)
js.tuiXingjianyue(x, Mercury)
js.tuiZhongci(x, Mercury)
js.tuiZhiri(x, Mercury)
js.tuiShuori(x, Mercury)
js.tuiRuzhongci(x, Mercury)
js.tuiRuyueri(x, Mercury)
js.qiuXingjian(x, Mercury)
js.qiuXingjian(0, Mercury)
