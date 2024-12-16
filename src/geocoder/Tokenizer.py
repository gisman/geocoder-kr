import re
import sys
from .tokens import *
from .util.HSimplifier import HSimplifier


class Tokenizer:
    """
    Tokenizer 클래스는 주소 문자열을 토큰화하고, 각 토큰의 유형을 추정하는 기능을 제공합니다.

    Attributes:
        hSimplifier (HSimplifier): HSimplifier 객체.
        re_tokenize_split (re.Pattern): 주소 문자열을 토큰으로 분리하기 위한 정규 표현식.
        re_tokenize_h2h4 (re.Pattern): H2와 H4 토큰을 추출하기 위한 정규 표현식.
        re_tokenize_ga (re.Pattern): '가' 또는 '번'으로 끝나는 도로명을 추출하기 위한 정규 표현식.
        re_tokenize_ga_only (re.Pattern): '가'로 끝나는 도로명을 추출하기 위한 정규 표현식.
        re_tokenize_road_num (re.Pattern): 도로명과 숫자를 추출하기 위한 정규 표현식.
        re_tokenize_road_num_err (re.Pattern): 도로명과 숫자 사이의 오타를 추출하기 위한 정규 표현식.
        re_bunji_n_n_bng (re.Pattern): 완결된 지번을 추출하기 위한 정규 표현식.
        re_bunji_n_의_n (re.Pattern): '의'가 포함된 지번을 추출하기 위한 정규 표현식.
        re_bunji_번지_호 (re.Pattern): '번지'와 '호'가 포함된 지번을 추출하기 위한 정규 표현식.
        re_bunji_n_n_호 (re.Pattern): '호'가 포함된 지번을 추출하기 위한 정규 표현식.
        re_bunjihead_n_n_bng (re.Pattern): 완결된 지번의 헤드를 추출하기 위한 정규 표현식.
        re_bunjihead_n_의_n (re.Pattern): '의'가 포함된 지번의 헤드를 추출하기 위한 정규 표현식.
        re_bunjihead_번지_호 (re.Pattern): '번지'와 '호'가 포함된 지번의 헤드를 추출하기 위한 정규 표현식.
        re_bunjihead_n_n_호 (re.Pattern): '호'가 포함된 지번의 헤드를 추출하기 위한 정규 표현식.
        re_bunjihead_n_호 (re.Pattern): '호'가 포함된 지번의 헤드를 추출하기 위한 정규 표현식.
        re_bunjihead_n_번지 (re.Pattern): '번지'가 포함된 지번의 헤드를 추출하기 위한 정규 표현식.
        re_지하건번 (re.Pattern): '지하'가 포함된 건번을 추출하기 위한 정규 표현식.
        re_bunji_n_호 (re.Pattern): '호'가 포함된 미완성 지번을 추출하기 위한 정규 표현식.
        re_bunji_n_번지 (re.Pattern): '번지'가 포함된 미완성 지번을 추출하기 위한 정규 표현식.
        re_층 (re.Pattern): 층 정보를 추출하기 위한 정규 표현식.
        re_건물호 (re.Pattern): 건물 호수를 추출하기 위한 정규 표현식.
        h1Prefix (list): H1 접두사를 정렬한 리스트.
        h23Prefix (list): H2와 H3 접두사를 정렬한 리스트.
        __h3 (dict): H3 정보를 담고 있는 딕셔너리.
        re_dong_읍면동 (re.Pattern): 읍, 면, 동 정보를 추출하기 위한 정규 표현식.
        re_dong_1동 (re.Pattern): '1동' 정보를 추출하기 위한 정규 표현식.
        re_dong_동_dot_동 (re.Pattern): '동.동' 정보를 추출하기 위한 정규 표현식.
        re_dong_숫자동_dot_숫자동 (re.Pattern): '숫자동.숫자동' 정보를 추출하기 위한 정규 표현식.
        re_dong_남대문로 (re.Pattern): 남대문로 정보를 추출하기 위한 정규 표현식.
        re_dong_세종로 (re.Pattern): 세종로 정보를 추출하기 위한 정규 표현식.
        re_dong_출장소 (re.Pattern): 출장소 정보를 추출하기 위한 정규 표현식.
        re_dong_10동 (re.Pattern): '10동' 정보를 추출하기 위한 정규 표현식.
        re_dong_6자동 (re.Pattern): '6자동' 정보를 추출하기 위한 정규 표현식.
        re_dong_종로1234가동 (re.Pattern): '종로1234가동' 정보를 추출하기 위한 정규 표현식.
        h4Prefix (list): H4 접두사를 정렬한 리스트.
        re_n동 (re.Pattern): 'n동' 정보를 추출하기 위한 정규 표현식.
        hd2ch (set): 동 정보를 담고 있는 집합.
        re_road_이름1길 (re.Pattern): 도로명 정보를 추출하기 위한 정규 표현식.
        re_road_이름1길2 (re.Pattern): 도로명 정보를 추출하기 위한 정규 표현식.
        re_road_이름길 (re.Pattern): 도로명 정보를 추출하기 위한 정규 표현식.
        re_road_공단길 (re.Pattern): 공단길 정보를 추출하기 위한 정규 표현식.
        re_road_산단길 (re.Pattern): 산단길 정보를 추출하기 위한 정규 표현식.
        re_road_숫자_숫자길 (re.Pattern): 숫자와 숫자가 포함된 도로명 정보를 추출하기 위한 정규 표현식.
        re_road_숫자길 (re.Pattern): 숫자가 포함된 도로명 정보를 추출하기 위한 정규 표현식.
        re_road_거리 (re.Pattern): 거리 정보를 추출하기 위한 정규 표현식.
        re_road_ETC길 (re.Pattern): 기타 도로명 정보를 추출하기 위한 정규 표현식.
        roadPrefix (list): 도로명 접두사를 정렬한 리스트.
        numRoadPatterns (list): 숫자로 시작하는 도로명 패턴을 담고 있는 리스트.

    Methods:
        __mergebrackets(toks, sep=" "): 괄호로 묶인 토큰을 하나로 병합합니다.
        __assumeTokenType(toks, ambiguous_only=False): 각 토큰의 유형을 추정합니다.
        __removeWhiteSpaces(toks): 토큰에서 공백을 제거합니다.
        __removeDotChar(toks): 토큰에서 점(.) 문자를 제거합니다.
        tokenize(address): 주소 문자열을 토큰화하고 각 토큰의 유형을 추정합니다.
        __isNumRoad(nm): 숫자로 시작하는 도로명인지 확인합니다.
        __hasH3(toks): H3 토큰이 있는지 확인합니다.
        hasH3(toks): H3 토큰이 있는지 확인합니다.
        __isH1(h1): H1 토큰인지 확인합니다.
        __splitH1(toks): H1 토큰을 분리합니다.
        __splitH2(toks, h2pos=None): H2 토큰을 분리합니다.
        __mergeTokenSequence(toks, fromSeq, toSeq): 토큰 시퀀스를 병합합니다.
        __mergeAdjacentTokens(toks, t, sep=" "): 인접한 토큰을 병합합니다.
        __splitH4(toks, h4pos): H4 토큰을 분리합니다.
        __isRoad(val): 도로명인지 확인합니다.
        __splitRoad(toks, roadpos): 도로명 토큰을 분리합니다.
        __splitUnder(toks, underpos): '지하' 토큰을 분리합니다.
        printToks(toks): 토큰을 출력합니다.
        getToksString(toks): 토큰을 문자열로 반환합니다.
    """

    def __init__(self):
        self.hSimplifier = HSimplifier()
        self.re_tokenize_split = re.compile(r"([\s()\[\],?])")
        # self.re_tokenize_split = re.compile(r'\s|,|\?')

        self.re_tokenize_h2h4 = re.compile(r"^(.{1,4}구)(.{1,5}동)(.+)")
        self.re_tokenize_ga = re.compile(r"^\d+(가|번)?[길로동]$")
        self.re_tokenize_ga_only = re.compile(r"^\d+가$")
        self.re_tokenize_road_num = re.compile(r"[로길동가]\d+(-\d+)?$")
        self.re_tokenize_road_num_err = re.compile(
            r"(\D+(\d+)?[로길가])\d+(-\d+)?$"
        )  # 청룡로11 띄어쓰기 오타

        # 완결된 지번
        self.re_bunji_n_n_bng = re.compile(r"^산?\d+-\d+(번지)?$")  # 1-2(번지)
        self.re_bunji_n_의_n = re.compile(r"^산?\d+의\d+(번지)?$")  # 1의2(번지)
        self.re_bunji_번지_호 = re.compile(r"^산?\d+번지\d+(호)?$")  # 1번지2(호)
        self.re_bunji_n_n_호 = re.compile(r"^산?\d+-\d+호$")  # 1013-6호

        self.re_bunjihead_n_n_bng = re.compile(r"^산?\d+-\d+(번지)?")  # 1-2(번지)
        self.re_bunjihead_n_의_n = re.compile(r"^산?\d+의\d+(번지)?")  # 1의2(번지)
        self.re_bunjihead_번지_호 = re.compile(r"^산?\d+번지\d+(호)?")  # 1번지2(호)
        self.re_bunjihead_n_n_호 = re.compile(r"^산?\d+-\d+호")  # 1013-6호
        self.re_bunjihead_n_호 = re.compile(r"^산?\d+호")  # 6호
        self.re_bunjihead_n_번지 = re.compile(r"^산?\d+번지")  # 1번지

        # 붙은 지하
        self.re_지하건번 = re.compile(r"^(지하)\d")  # 지하130

        # 미완성 지번
        self.re_bunji_n_호 = re.compile(r"^산?\d+호$")  # 6호
        self.re_bunji_n_번지 = re.compile(r"^산?\d+번지$")  # 1번지

        self.re_층 = re.compile(r"^지?.{1,2}층$")
        self.re_건물호 = re.compile(r"^(B-?)?\d{1,4}호$")  # B-1111호

        self.h1Prefix = self.hSimplifier.getSortedH1Prefic()
        # self.h1Prefix = sorted(list(self.__h1Dic.keys()), key=len, reverse=True)

        self.h23Prefix = [
            re.compile(r"^(서|동|남|북|중)구"),
            re.compile(r"^\S\S(시|군|구)"),
            re.compile(r"^\S\S\S(시|구)"),
            re.compile(r"^\S\S시\S\S구"),
            re.compile(r"^포항시?\s?(남|북)구"),
            re.compile(r"^고양시?\s?일산\s?(동|서)구"),
            re.compile(r"^창원시?\s?마산\s?(회원|합포)구"),
        ]

        self.__h3 = {
            "고양시": ("덕양구", "일산동구", "일산서구"),
            "고양": ("덕양구", "일산동구", "일산서구"),
            "성남시": ("분당구", "수정구", "중원구"),
            "성남": ("분당구", "수정구", "중원구"),
            "수원시": ("권선구", "영통구", "장안구", "팔달구"),
            "수원": ("권선구", "영통구", "장안구", "팔달구"),
            "안산시": ("단원구", "상록구"),
            "안산": ("단원구", "상록구"),
            "안양시": ("동안구", "만안구"),
            "안양": ("동안구", "만안구"),
            "용인시": ("기흥구", "수지구", "처인구"),
            "용인": ("기흥구", "수지구", "처인구"),
            "전주시": ("덕진구", "완산구"),
            "전주": ("덕진구", "완산구"),
            "창원시": ("마산합포구", "마산회원구", "성산구", "의창구", "진해구"),
            "창원": ("마산합포구", "마산회원구", "성산구", "의창구", "진해구"),
            "천안시": ("동남구", "서북구"),
            "천안": ("동남구", "서북구"),
            "청주시": ("상당구", "서원구", "청원구", "흥덕구"),
            "청주": ("상당구", "서원구", "청원구", "흥덕구"),
            "포항시": ("남구", "북구"),
            "포항": ("남구", "북구"),
        }

        # 동 명칭
        self.re_dong_읍면동 = re.compile(
            r"^\D{2,4}(읍|면|동)"
        )  # 가락동, 가락본동, 가사문학면
        self.re_dong_1동 = re.compile(
            r"^\D{1,3}동?제?\d(읍|면|동|가)"
        )  # 가락1동, 가야제1동, 남문로1가, 교1동
        self.re_dong_동_dot_동 = re.compile(
            r"^\D+\.\D+동"
        )  # 성내.충인동, 성화.개신.죽림동
        self.re_dong_숫자동_dot_숫자동 = re.compile(
            r"^\D{2,3}\d(\.|,)\S{1,2}동"
        )  # 종로5.6가동
        self.re_dong_남대문로 = re.compile(r"^남대문로?\d(가|동|가동)")
        self.re_dong_세종로 = re.compile(r"^(세종|시장북)로")
        self.re_dong_출장소 = re.compile(r"^\D+출장소?")
        self.re_dong_10동 = re.compile(r"^(대명|상계)1\d동")
        self.re_dong_6자동 = re.compile(r"^(야음|왕십)\S{3}동?")
        self.re_dong_종로1234가동 = re.compile(r"^종로1(\d|\.)+(가동?|동)")
        self.h4Prefix = [
            self.re_dong_읍면동,
            self.re_dong_1동,
            self.re_dong_동_dot_동,
            self.re_dong_숫자동_dot_숫자동,
            self.re_dong_남대문로,
            self.re_dong_세종로,
            self.re_dong_출장소,
            self.re_dong_10동,
            self.re_dong_6자동,
            self.re_dong_종로1234가동,
        ]

        self.re_n동 = re.compile(r"^\d동$")

        self.hd2ch = set(
            [
                "동읍",
                "겸면",
                "남면",
                "내면",
                "목면",
                "북면",
                "상면",
                "서면",
                "용면",
                "율면",
                "입면",
                "중면",
                "동면",
                "갑동",
                "강동",
                "경동",
                "계동",
                "교동",
                "구동",
                "국동",
                "궁동",
                "궐동",
                "금동",
                "길동",
                "남동",
                "내동",
                "능동",
                "다동",
                "달동",
                "답동",
                "당동",
                "대동",
                "덕동",
                "도동",
                "동동",
                "두동",
                "마동",
                "명동",
                "목동",
                "묘동",
                "묵동",
                "방동",
                "배동",
                "번동",
                "법동",
                "변동",
                "본동",
                "봉동",
                "부동",
                "북동",
                "사동",
                "삼동",
                "상동",
                "서동",
                "석동",
                "선동",
                "성동",
                "세동",
                "송동",
                "수동",
                "순동",
                "시동",
                "신동",
                "안동",
                "양동",
                "역동",
                "연동",
                "영동",
                "오동",
                "옥동",
                "와동",
                "왕동",
                "외동",
                "용동",
                "우동",
                "원동",
                "유동",
                "율동",
                "이동",
                "인동",
                "일동",
                "임동",
                "작동",
                "장동",
                "재동",
                "저동",
                "전동",
                "정동",
                "좌동",
                "죽동",
                "중동",
                "지동",
                "직동",
                "창동",
                "천동",
                "청동",
                "초동",
                "추동",
                "탑동",
                "통동",
                "파동",
                "평동",
                "포동",
                "풍동",
                "필동",
                "하동",
                "학동",
                "합동",
                "항동",
                "행동",
                "향동",
                "현동",
                "혈동",
                "호동",
                "화동",
                "효동",
                "흥동",
            ]
        )

        # 길명칭
        self.re_road_이름1길 = re.compile(
            r"^\D{1,7}\d{1,4}번?(길|로)"
        )  # 성정1길, 시민로24번길
        self.re_road_이름1길2 = re.compile(
            r"^.{2,5}\d{1,3}(번|로)?(가|나|다|라|마|바|사|아|자|동|서|남|북|안|번|\d)길"
        )  # 사당로29가길
        self.re_road_이름길 = re.compile(r"^\D{1,7}(길|로)")  # 초대로
        self.re_road_공단길 = re.compile(
            r"^(.+)?\d?공단지?(로|길)?(\d(길|대로|로))?"
        )  # 제2공단2길
        self.re_road_산단길 = re.compile(
            r"^.+(산단|첨단산업|산업단지)(\d+)?(길|로)(\d{1,3})?번?가?길?"
        )  # 군포첨단산업2로8번길, 2산단1길
        # self.re_road_길 = re.compile(r'^.+\d+(번안|번|안|리)?(가|나|다|라|마|바|사|아|자|차|카|상|하)?길')
        self.re_road_숫자_숫자길 = re.compile(
            r"^.{1,7}\d+(강로|로|번안|번|안|리)\d+번?(가|나|다|라|마|바|사|아|자|차|카|상|하|안)?길"
        )  # 김포한강10로133번길
        self.re_road_숫자길 = re.compile(
            r"^\S{1,7}\d{1,3}(가|나|다|라|마|차|카|리|번|번안|안|번가|번나|상|하|번상|번하)길"
        )  # 목동중앙남로14가길
        self.re_road_거리 = re.compile(
            r"^.{2,5}거리길?"
        )  # 가구거리, 젊음의1거리. 매우 소수
        self.re_road_ETC길 = re.compile(r"^.{1,11}(로|길|고개)")  # 기타 100여개
        self.roadPrefix = [
            self.re_road_이름1길,
            self.re_road_이름1길2,
            self.re_road_이름길,
            self.re_road_공단길,
            self.re_road_산단길,
            self.re_road_숫자_숫자길,
            self.re_road_숫자길,
            self.re_road_거리,
            self.re_road_ETC길,
        ]

        # 숫자로 시작하는 길이름
        self.numRoadPatterns = [
            "10용사",
            "1100로",
            "1공단",
            "1농공",
            "1순환",
            "2.28길",
            "2공단",
            "2번도로",
            "2산단",
            "2순환",
            "2함대",
            "3.1",
            "318만세",
            "3공단",
            "3산단",
            "3순환",
            "4.19",
            "419",
            "4.4만세",
            "44만세",
            "40계단",
            "4공단",
            "4산단",
            "5공단",
            "5산단",
            "516",
            "5일시장",
            "5일장",
            "63로",
            "8부두",
        ]

    def __mergebrackets(self, toks, sep=" "):
        """
        괄호로 묶인 토큰을 병합합니다.

        이 메서드는 토큰 목록을 끝에서 시작으로 스캔하여 여는 괄호와 닫는 괄호 쌍을 찾습니다.
        쌍이 발견되면 괄호를 포함하여 괄호 사이의 토큰을 하나의 토큰으로 병합합니다.

        매개변수:
            toks (Tokens): 처리할 토큰 목록입니다.
            sep (str, 선택적): 토큰을 병합할 때 사용할 구분자입니다. 기본값은 " "입니다.

        반환값:
            None
        """
        for n2 in range(len(toks) - 1, 1, -1):
            if toks.isBracketEnd(n2):
                for n1 in range(n2, 1, -1):
                    if toks.isBracketBegin(n1):
                        toks.merge(n1, n2 + 1, TOKEN_EXTRA, sep)
                        # s = ' '.join(toks[n1:n2+1])
                        # del toks[n1:n2+1]
                        # toks.insert(n1, s)
                        return

    def __assumeTokenType(self, toks, ambiguous_only=False):
        """
        주어진 토큰 목록(toks)을 기반으로 각 토큰의 유형을 추정합니다.

        Args:
            toks (list): 토큰 객체의 목록입니다.
            ambiguous_only (bool, optional): True로 설정하면, 모호한 토큰만 유형을 추정합니다. 기본값은 False입니다.

        Notes:
            - 함수는 토큰의 값과 이전 토큰의 유형을 기반으로 토큰 유형을 설정합니다.
            - 특정 규칙에 따라 토큰 유형을 결정합니다. 예를 들어, 토큰 값이 "시", "군", "구"로 끝나면 TOKEN_H23 유형으로 설정됩니다.
            - 함수는 지번, 도로명, 건물 번호 등의 다양한 유형을 처리합니다.
            - 함수는 토큰의 이전 유형(prevType)과 콤마 여부(beforeComma)를 추적하여 올바른 유형을 설정합니다.
            - 함수는 완전한 지번이 추출되었는지 여부(bngComplete)를 추적하여 이후 지번 판단에 사용합니다.
        """
        pos: int = 0

        prevType: str = "HEAD"
        beforeComma: bool = True
        bngComplete: bool = False  # 완전한 지번 추출됨. 이후 지번으로 판단하지 말 것
        for pos in range(len(toks)):
            tkn = toks.get(pos)

            if ambiguous_only and tkn.t not in (
                TOKEN_UNKNOWN,
                TOKEN_NUMERIC,
                TOKEN_COMMA,
                TOKEN_EXTRA,
            ):
                prevType = tkn.t
                continue

            if self.__isH1(tkn.val):  # h1
                if pos == 0 and tkn.val.startswith("세종"):
                    tkn.val = "세종"
                    tkn.t = TOKEN_H23
                else:
                    tkn.t = TOKEN_H1

            elif (
                tkn.val.endswith(("시", "군", "구"))
                and beforeComma
                and prevType in (TOKEN_H1, TOKEN_H23, "HEAD")
            ):  # h2
                tkn.t = TOKEN_H23

            elif (
                tkn.val.endswith(("읍", "면", "동"))
                and beforeComma
                and prevType in ("HEAD", TOKEN_H1, TOKEN_H23)
            ):  # h4
                tkn.t = TOKEN_H4

            elif (
                tkn.val.endswith("리") and beforeComma and prevType in (TOKEN_H4)
            ):  # h5
                tkn.t = TOKEN_RI

            elif (
                (tkn.val.endswith(("로", "길", "가", "거리")) or tkn.val == "계변고개")
                and beforeComma
                and prevType
                in (
                    TOKEN_H1,
                    TOKEN_H23,
                    TOKEN_H4,
                    TOKEN_RI,
                    TOKEN_ROAD,
                    TOKEN_BLD,
                    TOKEN_UNKNOWN,
                )
            ):  # 길이름
                if not tkn.val.endswith("상가"):  # 상가$ 제외
                    tkn.t = TOKEN_ROAD

            # 청룡로11
            elif (
                self.re_tokenize_road_num_err.match(tkn.val)
                and beforeComma
                and prevType in (TOKEN_H23, TOKEN_H4, TOKEN_RI)
            ):  # 길이름
                tkn.t = TOKEN_ROAD

            elif (
                self.re_bunji_n_n_bng.match(tkn.val)
                or self.re_bunji_n_의_n.match(tkn.val)
                or self.re_bunji_번지_호.match(tkn.val)
                or self.re_bunji_n_n_호.match(tkn.val)
            ):  # 완결된 지번 (지번 or 건번 or 동호)
                if prevType in (TOKEN_ROAD, TOKEN_UNDER):
                    tkn.t = TOKEN_BLDNO
                elif beforeComma and prevType not in (
                    TOKEN_BLDNO,
                    TOKEN_BLD,
                    TOKEN_BLD_DONG,
                    TOKEN_UNKNOWN,
                    "HEAD",
                ):
                    tkn.t = TOKEN_BNG
                    bngComplete = True
                else:
                    tkn.t = TOKEN_EXTRA

            elif tkn.val.startswith("지하"):
                if prevType == TOKEN_ROAD:
                    tkn.t = TOKEN_UNDER

            # 미완성 지번
            elif self.re_bunji_n_번지.match(tkn.val) or self.re_bunji_n_호.match(
                tkn.val
            ):  # 1번지
                if prevType in (
                    TOKEN_ROAD,
                    TOKEN_UNDER,
                ):  # 지번 또는 건번
                    tkn.t = TOKEN_BLDNO
                else:
                    if bngComplete or prevType == TOKEN_EXTRA:
                        tkn.t = TOKEN_BLD_HO
                    elif prevType in (
                        TOKEN_H4,
                        TOKEN_RI,
                    ):
                        tkn.t = TOKEN_BNG
                    elif prevType == TOKEN_BNG:
                        if toks.prev(pos).val.isnumeric():
                            # 1 2호
                            # 1 2
                            tkn.t = TOKEN_BLD_HO
                        else:
                            # 1번지 2호
                            tkn.t = TOKEN_BNG

            elif tkn.val.isnumeric() and prevType in (
                TOKEN_H4,
                TOKEN_RI,
            ):  # 숫자
                tkn.t = TOKEN_BNG

            elif tkn.val.isnumeric() and prevType in (
                TOKEN_ROAD,
                TOKEN_UNDER,
            ):  # 숫자
                tkn.t = TOKEN_BLDNO

            elif tkn.val.isnumeric() and prevType in (TOKEN_SAN):  # 숫자
                tkn.t = TOKEN_BNG

            elif tkn.val.isnumeric():  # 숫자
                tkn.t = TOKEN_NUMERIC

            elif tkn.val in (",", "."):  # ,
                tkn.t = TOKEN_COMMA
                beforeComma = False

            elif (
                tkn.val == "?"
                and not beforeComma
                and prevType
                in (
                    TOKEN_BNG,
                    TOKEN_BLDNO,
                    TOKEN_FLOOR,
                    TOKEN_NUMERIC,
                )
            ):  # ?
                tkn.t = TOKEN_COMMA
                beforeComma = False

            elif tkn.val.startswith("(") and tkn.val.endswith(")"):
                tkn.t = TOKEN_EXTRA

            elif not tkn.val.isnumeric() and prevType in (
                TOKEN_BNG,
                TOKEN_BLDNO,
            ):
                tkn.t = TOKEN_BLD

            elif not tkn.val.isnumeric() and prevType == TOKEN_BLD:
                tkn.t = TOKEN_BLD_DONG

            elif not tkn.val.isnumeric() and prevType in (
                TOKEN_H4,
                TOKEN_RI,
            ):
                if tkn.val == "산":
                    tkn.t = TOKEN_SAN
                elif re.match(r"^산?\d+의?\d+(번지)?", tkn.val):
                    tkn.t = TOKEN_BNG
                else:
                    tkn.t = TOKEN_BLD

            elif self.re_층.match(tkn.val):
                tkn.t = TOKEN_FLOOR

            elif self.re_n동.match(tkn.val) and prevType in (TOKEN_UNKNOWN):
                tkn.t = TOKEN_H4

            else:
                tkn.t = TOKEN_UNKNOWN

            prevType = tkn.t

    def __removeWhiteSpaces(self, toks):
        """
        주어진 토큰 리스트에서 공백 문자열을 제거합니다.

        매개변수:
        toks (list): 문자열 토큰의 리스트.

        반환값:
        없음
        """
        length = len(toks)
        for pos in reversed(range(length)):
            if toks[pos].strip() == "":
                toks.delete(pos)

    def __removeDotChar(self, toks):
        """
        주어진 토큰 목록에서 각 토큰의 끝에 있는 점(.) 문자를 제거합니다.

        매개변수:
        toks (list): 점(.) 문자를 제거할 토큰 객체의 목록입니다.

        반환값:
        없음
        """
        for n in range(len(toks)):
            tok = toks.get(n)
            if tok.val.endswith("."):
                tok.val = tok.val[:-1]

    def tokenize(self, address):
        """
        주어진 주소 문자열을 토큰화하여 Tokens 객체로 반환합니다.

        이 메서드는 주소 문자열을 여러 단계의 처리 과정을 통해 토큰화합니다.
        각 단계는 공백 제거, 특정 문자 제거, 괄호 묶기, 토큰 타입 추정, 인접 토큰 병합 등을 포함합니다.
        또한, 행정구역, 길, 번지, 건물번호 등의 특정 패턴을 인식하고 처리합니다.

        Args:
            address (str): 토큰화할 주소 문자열.

        Returns:
            Tokens: 토큰화된 주소를 포함하는 Tokens 객체.
        """
        toks = Tokens(self.re_tokenize_split.split(address))
        self.__removeWhiteSpaces(toks)
        self.__removeDotChar(toks)

        # 괄호 토큰 하나로 묶기
        self.__mergebrackets(toks)
        self.__assumeTokenType(toks)

        # H2, H3 (3차행정구역) 토큰 하나로 묶기
        self.__mergeAdjacentTokens(toks, TOKEN_H23, sep="")

        # H1 분리
        h1pos = toks.index(TOKEN_H1)
        if h1pos < 0:  # H1 없음
            self.__splitH1(toks)

        # H2 분리
        h2pos = toks.index(TOKEN_H23)
        if h2pos < 0 and toks.index(TOKEN_H4) and toks.index(TOKEN_ROAD):  # H2 없음
            h2pos = self.__splitH2(toks)

        if toks[h2pos] in self.__h3:
            # 3차행정구역 검사
            h2pos = self.__splitH2(toks, h2pos + 1)
            # H2, H3 (3차행정구역) 토큰 하나로 묶기
            self.__mergeAdjacentTokens(toks, TOKEN_H23, sep="")

        # H4 분리
        h4pos = toks.index(TOKEN_H4)
        if h4pos < 0 and toks.index(TOKEN_ROAD) < 0:  # H4 없음. ROAD 없음
            h4pos = self.__splitH4(toks, h4pos)

        # 길 분리
        roadpos = toks.index(TOKEN_ROAD)
        if roadpos < 0 and toks.index(TOKEN_H4) < 0:  # H4 없음. ROAD 없음
            roadpos = self.__splitRoad(toks, roadpos)

        self.__assumeTokenType(toks)
        self.__mergeAdjacentTokens(toks, TOKEN_ROAD, sep="")

        # 번지 결합
        self.__mergeTokenSequence(
            toks,
            [TOKEN_SAN, TOKEN_BNG],
            [TOKEN_BNG, TOKEN_BNG],
        )
        self.__mergeAdjacentTokens(toks, TOKEN_BNG, sep="")

        # 건물번호 결합
        self.__mergeAdjacentTokens(toks, TOKEN_BLDNO, sep="")

        # 잘린 동명 결합
        begin = self.__mergeTokenSequence(
            toks,
            [TOKEN_H23, TOKEN_UNKNOWN, TOKEN_H4],
            [TOKEN_H23, TOKEN_H4, TOKEN_H4],
        )
        if begin > -1:
            self.__mergeAdjacentTokens(toks, TOKEN_H4, sep="")

        # 행정구역 suffix 생략 주소
        self.__mergeTokenSequence(
            toks,
            [
                TOKEN_H1,
                TOKEN_UNKNOWN,
                TOKEN_UNKNOWN,
                TOKEN_UNKNOWN,
                TOKEN_NUMERIC,
            ],
            [
                TOKEN_H1,
                TOKEN_H23,
                TOKEN_H23,
                TOKEN_H4,
                TOKEN_BNG,
            ],
        )

        self.__mergeTokenSequence(
            toks,
            [
                TOKEN_H1,
                TOKEN_UNKNOWN,
                TOKEN_UNKNOWN,
                TOKEN_NUMERIC,
            ],
            [TOKEN_H1, TOKEN_H23, TOKEN_H4, TOKEN_BNG],
        )

        # 월영동 16길. H4 ROAD. 띄어쓰기 검사
        if toks.index(TOKEN_H4) > 0 and toks.index(TOKEN_ROAD) > 0:
            roadTok = toks.get(toks.index(TOKEN_ROAD))
            if roadTok.val[0].isdigit() and not self.__isNumRoad(
                roadTok.val
            ):  # 숫자로 시작
                self.__mergeTokenSequence(
                    toks,
                    [TOKEN_H23, TOKEN_H4, TOKEN_ROAD],
                    [TOKEN_H23, TOKEN_ROAD, TOKEN_ROAD],
                )

        # 거창군 거창읍 하동 1길 9. BLD ROAD. 길이름 띄어쓰기 검사
        if (
            toks.index(TOKEN_H4) > 0
            and toks.index(TOKEN_BLD) > 0
            and toks.index(TOKEN_ROAD) > 0
        ):
            roadTok = toks.get(toks.index(TOKEN_ROAD))
            if roadTok.val[0].isdigit() and not self.__isNumRoad(
                roadTok.val
            ):  # 숫자로 시작
                self.__mergeTokenSequence(
                    toks,
                    [TOKEN_H4, TOKEN_BLD, TOKEN_ROAD],
                    [TOKEN_H4, TOKEN_ROAD, TOKEN_ROAD],
                )

        # 청룡로11. ROAD. 붙여쓰기 검사
        if toks.index(TOKEN_ROAD) > 0 and toks.index(TOKEN_BLDNO) < 0:
            roadPos = toks.index(TOKEN_ROAD)
            roadTok = toks.get(roadPos)
            m = self.re_tokenize_road_num_err.match(roadTok.val)  # 숫자로 시작
            if m:
                toks.split(roadPos, len(m.group(1)), TOKEN_ROAD, TOKEN_BLDNO)

        # 길이름 있고 건번 없으면, ROAD-COMMA-NUMERIC
        if toks.index(TOKEN_ROAD) > 0 and toks.index(TOKEN_BLDNO) < 0:
            self.__mergeTokenSequence(
                toks,
                [TOKEN_ROAD, TOKEN_COMMA, TOKEN_NUMERIC],
                [TOKEN_ROAD, TOKEN_COMMA, TOKEN_BLDNO],
            )

        # 지하 UNDER 붙여쓰기 검사
        underpos = toks.index(TOKEN_UNDER)
        if underpos > 0:
            t = toks.get(underpos)
            m = self.re_지하건번.match(t.val)
            if m:
                toks.split(underpos, len(m.group(1)), TOKEN_UNDER, TOKEN_BLDNO)

        # 길이름 있고 건번 없으면, ROAD-UNKNOWN
        if toks.index(TOKEN_ROAD) > 0 and toks.index(TOKEN_BLDNO) < 0:
            self.__mergeTokenSequence(
                toks,
                [TOKEN_ROAD, TOKEN_UNKNOWN],
                [TOKEN_ROAD, TOKEN_BLD],
            )

            self.__mergeTokenSequence(
                toks,
                [TOKEN_ROAD, TOKEN_UNKNOWN],
                [TOKEN_ROAD, TOKEN_BLD],
            )

        # 길이름 분리, 건번과 붙음. 고골길 178번길73
        if toks.index(TOKEN_ROAD) > 0 and toks.index(TOKEN_BLDNO) < 0:
            pos = toks.index(TOKEN_BLD)
            if pos == toks.index(TOKEN_ROAD) + 1:  # ROAD BLD
                s = toks.get(pos).val
                # 102길11-5
                m = re.match(r"(^\d+번?길)\d", s)
                if m:
                    toks.split(pos, m.span(1)[1], TOKEN_ROAD, TOKEN_UNKNOWN)

                # 신월로 338원빌딩
                if not m:
                    m = re.match(r"(^\d+)\D+", s)
                    if m:
                        toks.split(pos, m.span(1)[1], TOKEN_BLDNO, TOKEN_UNKNOWN)

        # H23-UNKNOWN-ROAD
        self.__mergeTokenSequence(
            toks,
            [TOKEN_H23, TOKEN_UNKNOWN, TOKEN_ROAD],
            [TOKEN_H23, TOKEN_ROAD, TOKEN_ROAD],
        )
        self.__mergeAdjacentTokens(toks, TOKEN_ROAD, sep="")

        # H1-UNKNOWN-ROAD  서울 동대문 고미술로
        self.__mergeTokenSequence(
            toks,
            [TOKEN_H1, TOKEN_UNKNOWN, TOKEN_ROAD],
            [TOKEN_H1, TOKEN_H23, TOKEN_ROAD],
        )

        # 주민센터건물명 강서구 대저2동 대저2동 주민센터
        bldpos = toks.index(TOKEN_BLD)
        if bldpos > 0 and h4pos > 0:
            if toks[bldpos] == toks[h4pos]:

                toks.delete(bldpos)
                self.__mergeTokenSequence(
                    toks,
                    [TOKEN_H4, TOKEN_BLD_DONG],
                    [TOKEN_H4, TOKEN_BLD],
                )

        # 다시 assume
        self.__assumeTokenType(toks, ambiguous_only=True)

        return toks

    def __isNumRoad(self, nm):
        """
        주어진 문자열이 숫자 도로 패턴으로 시작하는지 확인합니다.

        Args:
            nm (str): 확인할 문자열.

        Returns:
            bool: 문자열이 숫자 도로 패턴으로 시작하면 True, 그렇지 않으면 False.
        """
        for pattern in self.numRoadPatterns:
            if nm.startswith(pattern):
                return True

        return False

    def __hasH3(self, toks):
        """
        주어진 토큰 목록에 특정 조건을 만족하는 H3 토큰이 있는지 확인합니다.

        Args:
            toks (list): 토큰 문자열의 리스트.

        Returns:
            bool: 조건을 만족하는 H3 토큰이 있으면 True, 그렇지 않으면 False.
        """
        if len(toks) < 4:
            return False

        return toks[1] in self.__h3 and not toks[2].endswith("동")

    def hasH3(self, toks):
        """
        주어진 토큰 목록에 H3가 포함되어 있는지 확인합니다.

        Args:
            toks (list): 토큰 목록

        Returns:
            bool: H3가 포함되어 있으면 True, 그렇지 않으면 False
        """
        return self.__hasH3(toks)

    def __isH1(self, h1: str) -> bool:  # h1
        """
        주어진 문자열이 H1인지 여부를 확인합니다.

        Args:
            h1 (str): 확인할 문자열.

        Returns:
            bool: 문자열이 H1이면 True, 그렇지 않으면 False.
        """
        return self.hSimplifier.isH1(h1)

    def __splitH1(self, toks):
        """
        주어진 토큰 목록에서 특정 조건에 따라 토큰을 분할합니다.

        Args:
            toks (TokenList): 토큰 목록 객체.

        Returns:
            None

        동작:
            - 첫 번째 토큰을 가져옵니다.
            - 토큰의 타입에 따라 길이 제한을 설정합니다.
            - 특정 조건에 맞는 토큰은 분할하지 않고 반환합니다.
            - 토큰의 길이가 길이 제한 이상인 경우, h1Prefix 목록에 있는 접두사로 시작하는지 확인하고,
              해당 접두사로 시작하면 토큰을 분할합니다.
        """
        tkn = toks.get(0)
        lenLimit = sys.maxsize
        if tkn.t == TOKEN_UNKNOWN:
            lenLimit = 8
        elif tkn.t == TOKEN_H23 and tkn.val.startswith("세종"):
            return
        elif tkn.t == TOKEN_H23 and tkn.val.startswith(
            ("광주시", "부산진구", "제주시")
        ):
            return
        elif tkn.t in (
            TOKEN_H23,
            TOKEN_H4,
            TOKEN_RI,
            TOKEN_ROAD,
        ):
            lenLimit = 4

        if len(tkn.val) >= lenLimit:
            for h1pref in self.h1Prefix:
                if tkn.val.startswith(h1pref):
                    toks.split(0, len(h1pref), TOKEN_H1, tkn.t)
                    break

    def __splitH2(self, toks, h2pos=None):
        """
        __splitH2 메서드는 주어진 토큰 리스트에서 특정 조건에 따라 토큰을 분할합니다.

        Args:
            toks (list): 토큰 객체의 리스트.
            h2pos (int, optional): 분할을 시작할 토큰의 위치. 기본값은 None이며, 이 경우 h1 토큰의 다음 위치가 사용됩니다.

        Returns:
            int: 분할이 완료된 후의 h2 토큰의 위치.
        """
        h1pos = toks.index(TOKEN_H1)
        if h2pos == None:
            h2pos = h1pos + 1  # h1 없으면 0, 있으면 next

        tkn = toks.get(h2pos)
        lenLimit = sys.maxsize
        if tkn.t == TOKEN_UNKNOWN:
            lenLimit = 6
        elif tkn.t in (TOKEN_H4, TOKEN_RI, TOKEN_ROAD):
            lenLimit = 4

        if len(tkn.val) >= lenLimit:
            for h23re in self.h23Prefix:
                m = h23re.match(tkn.val)
                if m:
                    toks.split(h2pos, m.span()[1], TOKEN_H23, tkn.t)
                    break

        return h2pos

    def __mergeTokenSequence(self, toks, fromSeq, toSeq):
        """
        __mergeTokenSequence 메서드는 주어진 토큰 시퀀스를 병합합니다.

        Args:
            toks (Tokenizer): 토큰 시퀀스를 포함하는 Tokenizer 객체.
            fromSeq (str): 병합할 시퀀스의 시작 타입.
            toSeq (str): 병합 후 변경할 시퀀스의 타입.

        Returns:
            int: 병합된 시퀀스의 시작 인덱스. 시퀀스를 찾지 못한 경우 -1을 반환합니다.
        """
        # 찾기 -> begin, end
        begin, end = toks.searchTypeSequence(fromSeq)
        # type 변경
        if begin > -1:
            toks.changeTypeSequence(begin, toSeq)

        return begin

    def __mergeAdjacentTokens(self, toks, t, sep=" "):
        """
        인접한 토큰을 병합합니다.

        Args:
            toks (list): 토큰 리스트.
            t (str): 병합할 토큰.
            sep (str, optional): 병합 시 사용할 구분자. 기본값은 " ".

        Returns:
            None
        """
        pos = toks.index(t)
        if pos > -1 and toks.index(t, pos + 1) == pos + 1:  # 바로 다음 토큰만 검사
            toks.merge(pos, pos + 2, t, sep)

    def __splitH4(self, toks, h4pos):
        """
        __splitH4 메서드는 주어진 토큰 리스트에서 특정 조건에 따라 토큰을 분할합니다.

        Args:
            toks (TokenList): 토큰 리스트 객체.
            h4pos (int): H4 토큰의 위치.

        Returns:
            int: 업데이트된 H4 토큰의 위치.

        동작:
            - 토큰 리스트에서 TOKEN_H23을 찾습니다.
            - TOKEN_H23이 존재하고 그 다음 위치가 리스트 범위 내에 있으면, H4 위치를 업데이트합니다.
            - 다음 토큰의 타입에 따라 길이 제한을 설정합니다.
            - 길이 제한에 따라 토큰을 분할할지 여부를 결정합니다.
            - 특정 조건을 만족하는 경우 토큰을 분할합니다.
        """
        h23pos = toks.index(TOKEN_H23)

        if h23pos > -1 and h23pos + 1 < len(toks):  # h2 없으면 포기, 있으면 next
            h4pos = h23pos + 1

            tkn = toks.get(h4pos)
            lenLimit = sys.maxsize
            if tkn.t == TOKEN_UNKNOWN:
                lenLimit = 5
            elif tkn.t in (TOKEN_RI, TOKEN_ROAD):
                lenLimit = 2

            splited = False
            if len(tkn.val) >= lenLimit:
                for re1 in self.h4Prefix:
                    m = re1.match(tkn.val)
                    if m:
                        toks.split(h4pos, m.span()[1], TOKEN_H4, tkn.t)
                        splited = True
                        break
            if (
                splited == False
                and len(tkn.val) > 2
                and tkn.val[2].isnumeric()
                and tkn.val[0:2] in self.hd2ch
            ):
                toks.split(h4pos, 2, TOKEN_H4, tkn.t)

        return h4pos

    def __isRoad(self, val):
        for re1 in self.roadPrefix:
            m = re1.match(val)
            if m:
                return m

        return None

    def __splitRoad(self, toks, roadpos):
        """
        __splitRoad 메서드는 주어진 토큰 리스트에서 도로 관련 토큰을 분리합니다.

        Args:
            toks (list): 토큰 객체의 리스트.
            roadpos (int): 도로 토큰의 위치.

        Returns:
            int: 업데이트된 도로 토큰의 위치.

        동작:
            - 토큰 리스트에서 TOKEN_H23을 찾습니다.
            - TOKEN_H23이 존재하고 그 다음 위치에 토큰이 있는 경우, 도로 토큰의 위치를 업데이트합니다.
            - 도로 토큰의 길이에 따라 길이 제한을 설정합니다.
            - 도로 접두사와 일치하는 경우, 해당 위치에서 토큰을 분리합니다.
        """
        h23pos = toks.index(TOKEN_H23)

        if h23pos > -1 and h23pos + 1 < len(toks):  # h2 없으면 포기, 있으면 next
            roadpos = h23pos + 1

            tkn = toks.get(roadpos)
            lenLimit = sys.maxsize
            if tkn.t == TOKEN_UNKNOWN:
                lenLimit = 5
            elif tkn.t in (TOKEN_RI, TOKEN_ROAD):
                lenLimit = 2

            if len(tkn.val) >= lenLimit:
                for re1 in self.roadPrefix:
                    m = re1.match(tkn.val)
                    if m:
                        toks.split(roadpos, m.span()[1], TOKEN_ROAD, tkn.t)
                        break
        return roadpos

    def __splitUnder(self, toks, underpos):
        """
        주어진 토큰 목록에서 특정 위치의 토큰이 TOKEN_UNDER인지 확인하고,
        해당 토큰이 지하 건물 번호 형식과 일치하면 토큰을 분할합니다.

        Args:
            toks (Tokens): 토큰 목록.
            underpos (int): 확인할 토큰의 위치.

        Returns:
            int: 처리된 토큰의 위치.
        """
        tkn = toks.get(underpos)
        if tkn.t == TOKEN_UNDER:
            m = self.re_지하건번.match(tkn.val)
            if m:
                toks.split(underpos, m.span()[1], TOKEN_UNDER, TOKEN_BLDNO)

        return underpos

    def printToks(self, toks):
        print(self.getToksString(toks))

    def getToksString(self, toks):
        """
        주어진 토큰 목록을 문자열로 변환합니다.

        Args:
            toks (TokenList): 토큰 객체의 목록.

        Returns:
            str: 각 토큰의 문자열 표현을 줄바꿈으로 구분한 문자열.
        """
        lines = []

        for i in range(len(toks)):
            tkn = toks.get(i)
            lines.append(f"{tkn.t}\t{tkn.val}")

        return "\n".join(lines)
