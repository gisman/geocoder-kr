import re


class BldSimplifier:
    def __init__(self):
        # 정규 표현식을 사용하여 단지 번호를 찾기 위한 패턴
        self.n단지 = re.compile(r"(\d{1,2})(차|단지)")

        # 건물 이름의 별칭을 매핑하기 위한 사전 생성
        self.BLD_ALIAS_MAP = self.build_alias_map(
            [
                ["더편한", "더-편한", "THE편한", "THE-편한"],
                ["E편한세상", "E-편한세상", "이편한세상", "이-편한세상"],
                ["자이", "XI"],
                ["래미안", "레미안"],
                ["레지던스", "레지던트"],
                ["아이파크", "I파크", "I파크", "I-PARK", "IPARK"],
                ["꿈에그린", "한화꿈에그린", "꿈의그린", "한화꿈의그린"],
            ]
        )

        # 삭제할 접미사 패턴 목록
        self.REMOVE_SUFFIX_REGEXP = [
            re.compile(r"\s|,|\?$"),
            re.compile(r"([가-하]|[A-G]|[a-g]|에이|비|비이|씨|씨이|디|디이|\d+)동$"),
            re.compile(r"([A-G]|[a-g]|에이|비|비이|씨|씨이|디|디이|\d+)지구$"),
            re.compile(r"원룸(텔)?$")
            # , re.compile(r'\d차$')
            ,
            re.compile(r"(일|이|삼|사|오|Ⅰ|Ⅱ|Ⅳ|)차$"),
            re.compile(r"\d+$"),
            re.compile(r"\)$"),
            re.compile(r"(A|B|C|에이|비)$"),
            re.compile(r"(힐)?스테이트$"),
            re.compile(r"(벨|팰|펠)리체$"),
            re.compile(r"(빌라)?(맨|멘)(숀|션)$"),
            re.compile(r"(펜|팬)(숀|션)$"),
            re.compile(r"(\d|[A-Z])(부|블)(럭|록)$"),
            # re.compile(r'[^A-Z]A$')
        ]

        # 삭제할 접미사 목록
        self.REMOVE_SUFFIX = sorted(
            [
                "APT",
                "@",
                "A.P.T",
                "아파트",
                "다세대주택",
                "연립주택",
                "다가구주택",
                "빌라",
                "주택",
                "뉴타운",
                "홈타운",
                "타운",
                "맨션",
                "연립",
                "다세대",
                "다가구",
                "공동주택",
                "하우스",
                "하우징",
                "빌리지",
                "빌",
                "하이츠",
                "빌라트",
                "빌라텔",
                "빌리지",
                "팰리스",
                "펠리스",
                "마을",
                "캐슬",
                "파크",
                "빌딩",
                "오피스텔",
                "I",
                "II",
                "Ⅰ",
                "Ⅱ",
                "PARK",
                "HILL",
                "VILL",
                "VILLE",
                "단지",
                "주상복합",
                "家",
                "카운티",
                "시티",
                "씨티",
                "스위트",
                "아트",
                "리빙텔",
                "타워",
                "하임",
                "프라임",
                "신축공사",
            ],
            key=len,
            reverse=True,
        )

    def simplifyBldName(self, nm):
        """
        건물 이름을 단순화하는 메서드
        :param nm: 건물 이름
        :return: 단순화된 건물 이름
        """
        # ...existing code...

        # 3차, 3단지
        danjiNo = ""
        m = self.n단지.search(nm)
        if m:
            danjiNo = m.group(1)
            nm = nm[: m.start()] + nm[m.end() :]

        for pattern in self.REMOVE_SUFFIX_REGEXP:
            nm = re.sub(pattern, "", nm)

        if nm in self.BLD_ALIAS_MAP:
            nm = self.BLD_ALIAS_MAP[nm]

        for i in range(
            3
        ):  # suffix 순서를 알 수 없으므로 3회 제거. ex)횡성팰리스파크아파트
            for suffix in self.REMOVE_SUFFIX:
                if nm.endswith(suffix):
                    nm = nm[: -len(suffix)]
                    break

        return nm + danjiNo

    def stripStartName(self, startNames, nm):
        """
        시작 이름을 제거하는 메서드
        :param startNames: 제거할 시작 이름 목록
        :param nm: 건물 이름
        :return: 시작 이름이 제거된 건물 이름
        """
        for pref in startNames:
            nm = self.longestPrefixRemove(pref, nm)

        return nm

    def stripHName(self, daddr, nm):
        """
        지역 이름을 제거하는 메서드
        :param daddr: 지역 정보 사전
        :param nm: 건물 이름
        :return: 지역 이름이 제거된 건물 이름
        """
        # 지역 prefix
        nm = self.longestPrefixRemove(daddr["h23_nm"], nm)
        nm = self.longestPrefixRemove(daddr["ld_nm"], nm)
        nm = self.longestPrefixRemove(daddr["h4_nm"], nm)
        nm = self.longestPrefixRemove(daddr["ri_nm"], nm)
        nm = self.longestPrefixRemove(daddr["road_nm"], nm)

        return nm

    def build_alias_map(self, bld_alias):
        """
        건물 이름의 별칭을 매핑하는 사전을 생성하는 메서드
        :param bld_alias: 별칭 목록
        :return: 별칭 매핑 사전
        """
        dic = {}
        for aliasset in bld_alias:
            nm = aliasset[0]
            for alias in aliasset:
                dic[alias] = nm
        return dic

    def longestPrefixRemove(self, prefix, nm):
        """
        가장 긴 접두사를 제거하는 메서드
        :param prefix: 접두사
        :param nm: 건물 이름
        :return: 접두사가 제거된 건물 이름
        """
        plen = min(len(prefix), len(nm))
        n = 0
        for i in range(plen):
            if prefix[i] != nm[i]:
                break
            n += 1

        if n < 2:
            return nm
        else:
            return nm[n:].strip()
