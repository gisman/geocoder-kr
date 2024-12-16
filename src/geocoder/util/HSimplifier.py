import re


class HSimplifier:
    # TAG_H2 = '@'
    # TAG_H3 = '#'
    # TAG_H4 = '$'
    # TAG_H5 = '%'

    # h2h3 포항시남구 -> 포항남
    h23re = re.compile(r"^(.+)(시)(.+)(구)$")

    # 시군구 산청군 -> 산청
    h2re = re.compile(r"^(.+)(시|군|구)$")

    re_dong_세종로 = re.compile(r"^(세종|시장북)로")
    re_dong_남대문로 = re.compile(r"^남대문로?(\d)(가|동|가동)$")
    re_dong_서제1동 = re.compile(
        r"^서제(\d)동?$"
    )  # 가락1동, 가야제1동, 남문로1가, 교1동
    re_dong_1동 = re.compile(
        r"^(\D{1,3})동?제?(\d)(읍|면|동|가)$"
    )  # 가락1동, 가야제1동, 남문로1가, 교1동
    re_dong_성수1가제1동 = re.compile(
        r"^성수(1|2)가제?(1|2)동?$"
    )  # 가락1동, 가야제1동, 남문로1가, 교1동
    re_dong_남산동1가 = re.compile(
        r"^(\D{1,3})동?제?(\d)가동?$"
    )  # 가락1동, 가야제1동, 남문로1가, 교1동
    re_dong_종로1234가동 = re.compile(
        r"^종로(\d{2,4})가?동?$"
    )  # 가락1동, 가야제1동, 남문로1가, 교1동
    re_dong_출장소 = re.compile(r"^(\D+출장)소?$")
    re_dong_읍면동 = re.compile(
        r"(^\D{2,4})(읍|면|동)$"
    )  # (가락)동, (가락본)동, (가사문학)면

    def __init__(self):
        """
        HSimplifier 클래스의 생성자입니다.
        지역 이름을 단순화하기 위한 사전(__h1Dic)을 초기화합니다.
        """
        self.__h1Dic = {
            "강원특별자치도": "강원",
            "강원자치도": "강원",
            "강원특별도": "강원",
            "강원도": "강원",
            "강원": "강원",
            "경기도": "경기",
            "경기": "경기",
            "경상남도": "경남",
            "경남": "경남",
            "경상북도": "경북",
            "경상븍도": "경북",
            "경북": "경북",
            "광주광역시": "광주",
            "광주시": "광주",
            "광주": "광주",
            "대구광역시": "대구",
            "대구시": "대구",
            "대구": "대구",
            "대전광역시": "대전",
            "대전시": "대전",
            "대전": "대전",
            "부산광역시": "부산",
            "부산시": "부산",
            "부산": "부산",
            "서울특별시": "서울",
            "서울시": "서울",
            "서울": "서울",
            "세종특별자치시": "세종",
            "세종자치시": "세종",
            "세종특별시": "세종",
            "세종시": "세종",
            "세종": "세종",
            "울산광역시": "울산",
            "울산시": "울산",
            "울산": "울산",
            "인천광역시": "인천",
            "인천시": "인천",
            "인천": "인천",
            "전라남도": "전남",
            "전남": "전남",
            "전북특별자치도": "전북",
            "전북자치도": "전북",
            "전북특별도": "전북",
            "전라북도": "전북",
            "전라븍도": "전북",
            "전북": "전북",
            "제주특별자치도": "제주",
            "제주자치도": "제주",
            "제주특별도": "제주",
            "제주도": "제주",
            "제주": "제주",
            "충청남도": "충남",
            "충남": "충남",
            "충청북도": "충북",
            "충북": "충북",
        }

    def getSortedH1Prefic(self):
        """
        __h1Dic의 키를 길이 내림차순으로 정렬하여 반환합니다.
        """
        return sorted(list(self.__h1Dic.keys()), key=len, reverse=True)

    def isH1(self, h1: str):
        """
        주어진 h1이 __h1Dic에 존재하는지 확인합니다.

        :param h1: 확인할 지역 이름
        :return: 존재하면 True, 그렇지 않으면 False
        """
        return h1 in self.__h1Dic

    def h1Hash(self, h1):
        """
        주어진 h1에 대응하는 해시을 반환합니다.

        :param h1: 단순화할 지역 이름
        :return: 지역 이름 해시
        """
        if h1 in self.__h1Dic:
            return self.__h1Dic[h1]
        else:
            return ""

    def h23Hash(self, h23):
        """
        주어진 h23에 대응하는 해시를 반환합니다.

        :param h23: 단순화할 지역 이름
        :return: 지역 이름 해시
        """
        # 양구군 예외
        if h23.startswith("양구"):
            return "양구"

        # h2h3 포항시남구 -> 포항남
        m = self.h23re.search(h23)
        if m:
            h23 = m.group(1) + m.group(3)

        # 시군구 산청군 -> 산청
        m = self.h2re.search(h23)
        if m:
            h23 = m.group(1)

        # 부천시 XX구 예외처리. 2015년 구 없앰.
        if h23.startswith("부천"):
            h23 = h23[:2]
        return h23

    def h4Hash(self, h4, keep_dong=False):
        """
        주어진 h4에 대응하는 해시를 반환합니다.

        :param h4: 단순화할 지역 이름
        :param keep_dong: '동'을 유지할지 여부
        :return: 지역 이름 해시
        """
        end_char = ""
        if keep_dong and h4.endswith("동"):
            end_char = "동"

        m = re.match(r"\S{2,}제\d동$", h4)
        if m:
            h4 = h4[0:-3] + h4[-3 + 1 :]

        # 별칭 단순화

        # 세종로
        # 시장북로
        # self.re_dong_세종로 = re.compile(r'^(세종|시장북)로')
        if self.re_dong_세종로.match(h4):
            return h4

        # 종로1.2.3.4가동, 종로1.2.3.4동 -> 종로1234
        # 비산2.3동, 비산2,3동 -> 비산23
        # 성화.개신.죽림동 -> 성화개신죽림
        if "." in h4 or "," in h4:
            h4 = h4.replace(".", "").replace(",", "")
            # return re.sub(r'(읍|면|동)$', '', h4) # 종로1234가동 -> 종로1234

        # 남대문로1가, 남대문로1가동, 남대문1가동 -> 남대문1가
        # self.re_dong_남대문로 = re.compile(r'^남대문로?(\d)(가|동|가동)$')
        m = self.re_dong_남대문로.search(h4)
        if m:
            return "남대문" + m.group(1) + "가"

        # 가야제1동, 가야1동 -> 가야1
        # 예외: 서제1동 -> 서1
        # self.re_dong_서제1동 = re.compile(r'^서제(\d)동?$')             # 가락1동, 가야제1동, 남문로1가, 교1동
        m = self.re_dong_서제1동.search(h4)
        if m:
            return f"서{m.group(1)}{end_char}"

        # 가야제1동, 가야1동 -> 가야1
        # self.re_dong_1동 = re.compile(r'^(\D{1,3})동?제?(\d)(읍|면|동|가)$')             # 가락1동, 가야제1동, 남문로1가, 교1동
        m = self.re_dong_1동.search(h4)
        if m:
            return m.group(1) + m.group(2) + end_char

        # 성수1가제1동, 성수1가1동 -> 성수1가1
        # self.re_dong_성수1가제1동 = re.compile(r'^성수(1|2)가제?(1|2)동?$')             # 가락1동, 가야제1동, 남문로1가, 교1동
        m = self.re_dong_성수1가제1동.search(h4)
        if m:
            return f"성수{m.group(1)}가{m.group(2)}{end_char}"

        # 남산동1가, 남산1가, 남산1가동 -> 남산1가
        # 남산1동 있음. 남산1동 -> 남산1
        # self.re_dong_남산동1가 = re.compile(r'^(\D{1,3})동?제?(\d)가동?$')             # 가락1동, 가야제1동, 남문로1가, 교1동
        m = self.re_dong_남산동1가.search(h4)
        if m:
            return f"{m.group(1)}{m.group(2)}가{end_char}"

        # self.re_dong_종로1234가동 = re.compile(r'^종로(\d{2,4})가?동?$')             # 가락1동, 가야제1동, 남문로1가, 교1동
        m = self.re_dong_종로1234가동.search(h4)
        if m:
            return f"종로{m.group(1)}{end_char}"

        # (흑산면대둔도출장), (가은읍북부출장)소
        # self.re_dong_출장소 = re.compile(r'^(\D+출장)소?$')
        m = self.re_dong_출장소.search(h4)
        if m:
            return m.group(1)

        # .+읍면동$ -> .+
        # self.re_dong_읍면동 = re.compile(r'(^\D{2,4})(읍|면|동)$')  # (가락)동, (가락본)동, (가사문학)면
        m = self.re_dong_읍면동.search(h4)
        if m:
            return m.group(1) + end_char

        return h4

    def h5Hash(self, h5):
        """
        주어진 h5에서 숫자를 제거하여 반환합니다.

        :param h5: 단순화할 지역 이름
        :return: 숫자가 제거된 지역 이름
        """
        return re.sub(r"\d", "", h5)
