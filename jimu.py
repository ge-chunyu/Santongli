class jimu:

    # 1. period: 小周
    # 2. cycle: 歲數
    # 3. jianZhongfa: 見中法
    # 4. jianzhongfen: 見中分 = 歲數 * 12
    # 5. jizhong: 積中 = 見中分 // 見中法
    # 6. zhongyu: 中餘 = 見中分 % 見中法
    # 7. jianRunfen: 見閏分 = 歲數 * 7
    # 8. jianYuefa: 見月法 = 見中法 * 19
    # 9. jiyue: 積月 = (歲數 * 235) // 見月法
    # 10. yueyu: 月餘 = (歲數 * 235) % 見月法
    # 11. jianYueRifa: 見月日法 = 見月法 * 日法 = 見月法 * 81
    # 12. jianZhongRifa: 見中日法 = 見月日法 * 3
    # 13. chenZhongfen: 晨中分 = 見中分 * 9 / 16
    # 14. chenJizhong: 晨積中 = 晨中分 // 見中法
    # 15. chenJizhong: 晨中餘 = 晨中分 % 見中法
    # 16. xiZhongfen: 夕中分 = 見中分 * 7 / 16
    # 17. chenJizhong: 夕積中 = 夕中分 // 見中法
    # 18. chenJizhong: 夕中餘 = 夕中分 % 見中法
    # 19. chenRunfen: 晨閏分 = 見閏分 * 9 / 16
    # 20. chenJiyue: 晨積月 = (歲數 * 235 * 9) // (見月法 * 16)
    # 21. chenYueyu: 晨月餘 = (歲數 * 235 * 9) % (見月法 * 16)
    # 22. xiRunfen: 夕閏分 = 見閏分 * 7 / 16
    # 23. xiJiyue: 夕積月 = (歲數 * 235 * 7) // (見月法 * 16)
    # 24. xiYueyu: 夕月餘 = (歲數 * 235 * 7) % (見月法 * 16)
    jimu = {
        'period': {'Jupiter': 12, 'Venus': 16, 'Saturn': 30,
                   'Mars': 64, 'Mercury': 64},
        'cycle': {'Jupiter': 1728, 'Venus': 3456, 'Saturn': 4320,
                  'Mars': 13824, 'Mercury': 9216},
        'jianZhongfa': {'Jupiter': 1583, 'Venus': 2161, 'Saturn': 4175,
                        'Mars': 6469, 'Mercury': 29041}}

    def __init__(self, mode="Jupiter"):
        self._mode = mode
        self.name = mode

    @property
    def cycle(self) -> float:
        # 歲數
        return self.jimu['cycle'][self._mode]

    @property
    def period(self) -> float:
        # 小周
        return self.jimu['period'][self._mode]

    @property
    def jianZhongfa(self) -> float:
        # 見中法
        return self.jimu['jianZhongfa'][self._mode]

    @property
    def jianzhongfen(self) -> float:
        # 見中分
        return self.cycle * 12

    @property
    def jizhong(self) -> float:
        # 積中
        return self.jianzhongfen // self.jianZhongfa

    @property
    def zhongyu(self) -> float:
        # 中餘
        return self.jianzhongfen % self.jianZhongfa

    @property
    def jianRunfen(self) -> float:
        # 見閏分
        return self.cycle * 7

    @property
    def jianYuefa(self) -> float:
        # 見月法
        return self.jianZhongfa * 19

    @property
    def jiyue(self) -> float:
        # 積月 = (歲數 * 235) // 見月法
        return (self.cycle * 235) // self.jianYuefa

    @property
    def yueyu(self) -> float:
        # 月餘 = (歲數 * 235) % 見月法
        return (self.cycle * 235) % self.jianYuefa

    @property
    def jianYueRifa(self) -> float:
        # 見月日法 = 見月法 * 日法 = 見月法 * 81
        return self.jianYuefa * 81

    @property
    def jianZhongRifa(self) -> float:
        # 見中日法 = 見月日法 * 3
        return self.jianYueRifa * 3

    @property
    def chenZhongfen(self) -> float:
        if self._mode in ["Mercury", "Venus"]:
            # 晨中分 = 見中分 * 9 / 16
            return self.jianzhongfen * 9 / 16

    @property
    def chenJizhong(self) -> float:
        if self._mode in ["Mercury", "Venus"]:
            # 晨積中 = 晨中分 // 見中法
            return self.chenZhongfen // self.jianZhongfa

    @property
    def chenZhongyu(self) -> float:
        if self._mode in ["Mercury", "Venus"]:
            # 晨中餘 = 晨中分 % 見中法
            return self.chenZhongfen % self.jianZhongfa

    @property
    def xiZhongfen(self) -> float:
        if self._mode in ["Mercury", "Venus"]:
            # 夕中分 = 見中分 * 7 / 16
            return self.jianzhongfen * 7 / 16

    @property
    def xiJizhong(self) -> float:
        if self._mode in ["Mercury", "Venus"]:
            # 夕積中 = 夕中分 // 見中法
            return self.xiZhongfen // self.jianZhongfa

    @property
    def xiZhongyu(self) -> float:
        if self._mode in ["Mercury", "Venus"]:
            # 夕中餘 = 夕中分 % 見中法
            return self.xiZhongfen % self.jianZhongfa

    @property
    def chenRunfen(self) -> float:
        if self._mode in ["Mercury", "Venus"]:
            # 晨閏分 = 見閏分 * 9 / 16
            return self.jianRunfen * 9 / 16

    @property
    def chenJiyue(self) -> float:
        if self._mode in ["Mercury", "Venus"]:
            # 晨積月 = (歲數 * 235 * 9) // (見月法 * 16)
            return (self.cycle * 235 * 9) // (self.jianYuefa * 16)

    @property
    def chenYueyu(self) -> float:
        if self._mode in ["Mercury", "Venus"]:
            # 晨中餘 = (歲數 * 235 * 9) % (見月法 * 16)
            return (self.cycle * 235 * 9) % (self.jianYuefa * 16)

    @property
    def xiRunfen(self) -> float:
        if self._mode in ["Mercury", "Venus"]:
            # 夕閏分 = 見閏分 * 7 / 16
            return self.jianRunfen * 7 / 16

    @property
    def xiJiyue(self) -> float:
        if self._mode in ["Mercury", "Venus"]:
            # 夕積月 = (歲數 * 235 * 7) // (見月法 * 16)
            return (self.cycle * 235 * 7) // (self.jianYuefa * 16)

    @property
    def xiYueyu(self) -> float:
        if self._mode in ["Mercury", "Venus"]:
            # 夕中餘 = (歲數 * 235 * 7) % (見月法 * 16)
            return (self.cycle * 235 * 7) % (self.jianYuefa * 16)
