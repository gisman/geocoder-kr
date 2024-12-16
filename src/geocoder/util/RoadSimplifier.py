import re


class RoadAliasChanger:
    """
    주어진 정규 표현식 패턴을 기반으로 도로 별칭을 정규 이름으로 변경하는 클래스입니다.

    속성:
        alias_regex (re.Pattern): 도로 별칭을 매칭하기 위한 컴파일된 정규 표현식 패턴입니다.
        regular_nm (str): 별칭을 대체할 정규 이름입니다.

    메서드:
        execute(nm):
            주어진 이름을 별칭 정규 표현식과 매칭하여 별칭을 정규 이름으로 대체합니다.
            매칭이 되면 새로운 이름을 반환하고, 그렇지 않으면 None을 반환합니다.
    """

    def __init__(self, alias_regex, regular_nm):
        """
        정규 표현식 패턴과 정규 이름으로 RoadAliasChanger를 초기화합니다.

        매개변수:
            alias_regex (re.Pattern): 도로 별칭을 매칭하기 위한 컴파일된 정규 표현식 패턴입니다.
            regular_nm (str): 별칭을 대체할 정규 이름입니다.
        """
        self.alias_regex = alias_regex
        self.regular_nm = regular_nm

    def execute(self, nm):
        """
        주어진 이름을 별칭 정규 표현식과 매칭하여 별칭을 정규 이름으로 대체합니다.

        매개변수:
            nm (str): 확인하고 잠재적으로 수정할 이름입니다.

        반환값:
            str: 매칭이 되면 별칭이 정규 이름으로 대체된 새로운 이름입니다.
            None: 매칭이 되지 않으면 None을 반환합니다.
        """
        m = self.alias_regex.match(nm)
        if m:
            # alias = m.group(1)
            newnm = self.regular_nm + nm[m.start(2) :]
            return newnm
        else:
            return None


class RoadSimplifier:
    """
    도로 이름을 단순화하는 클래스입니다.

    속성:
        alias_changer (list): 도로 이름의 별칭을 변경하는 RoadAliasChanger 객체의 리스트입니다.

    메서드:
        __init__(): RoadSimplifier 객체를 초기화합니다.
        roadHash(road): 주어진 도로 이름을 단순화하여 해시 값을 반환합니다.
    """

    # 별칭 map
    alias_changer = [
        RoadAliasChanger(
            re.compile(r"(서울시립대로)(.+)"), "시립대로"
        ),  # 서울시립대로14길 => 시립대로14길
    ]

    def __init__(self):
        """
        RoadSimplifier 객체를 초기화합니다.
        """
        pass

    def roadHash(self, road):
        """
        주어진 도로 이름을 단순화하여 해시 값을 반환합니다.

        매개변수:
            road (str): 단순화할 도로 이름입니다.

        반환값:
            str: 단순화된 도로 이름의 해시 값입니다.
        """
        if "·" in road:
            road = road.replace("·", ".")

        if road == "남산동1가":
            return "남산1가"

        for ac in self.alias_changer:
            road_new = ac.execute(road)
            if road_new:
                road = road_new
                break

        return road
