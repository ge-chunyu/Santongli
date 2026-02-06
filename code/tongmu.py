class tongmu:
    "統母"
    rifa: int = 81              # 日法
    runfa: int = 19             # 閏法
    tongfa: int = 1539          # 統法 = 日法 * 閏法
    yuanfa: int = 4617          # 元法 = 3 * 統法
    huishu: int = 47            # 會數
    zhangyue: int = 235         # 章月 = 12 * 19 + 7
    yuefa: int = 2392           # 月法 = 29 * 81 + 43
    tongfa: int = 598           # 通法 = 月法 * 中法
    zhongfa: int = 140530       # 中法 = 元法 * 12
    zhoutian: int = 562120      # 周天 = 章月 * 月法
    suizhong: int = 12          # 歲中
    yuezhou: int = 254          # 月周
    shuowangZhihui: int = 135   # 朔望之會
    huiyue: int = 6345          # 會月 = 會數 * 朔望之會
    tongyue: int = 19035        # 統月 = 日法 * 章月
    yuanyue: int = 57105        # 元月 = 3 * 統月
    zhangzhong: int = 228       # 章中 = 歲中 * 章歲/閏法
    tongzhong: int = 18468      # 統中 = 章中 * 日法
    yuanzhong: int = 55404      # 元中 = 3 * 統中
    ceyu: int = 8080            # 策餘 = 365 385/1539 - 360 = 8080/1539
    zhouzhi: int = 57           # 周至 = 3 * 章歲
