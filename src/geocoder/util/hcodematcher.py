import csv


class HCodeMatcher:
    def __init__(self):
        """
        HCodeMatcher 클래스 생성자.
        'db/code/h1_h2_code_match.csv' 파일을 읽어와서 hcode_dict 딕셔너리에 저장합니다.
        """
        filename = "db/code/h1_h2_code_match.csv"
        self.hcode_dict = {}
        with open(filename, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # 시도명,시군구명,시도코드,시군구코드,최신시도코드,최신시군구코드,비고,통계청 시도코드,통계청 시군구코드
                self.hcode_dict[row["시군구코드"]] = row

    def get_h2_cd(self, h2_cd):
        """
        주어진 시군구코드(h2_cd)에 해당하는 최신 시군구코드를 반환합니다.

        :param h2_cd: 시군구코드
        :return: 최신 시군구코드
        """
        return self.hcode_dict[h2_cd]["최신시군구코드"]

    def get_kostat_h1_cd(self, h2_cd):
        """
        주어진 시군구코드(h2_cd)에 해당하는 통계청 시도코드를 반환합니다.
        h2_cd가 None이거나 빈 문자열일 경우 빈 문자열을 반환합니다.

        :param h2_cd: 시군구코드
        :return: 통계청 시도코드
        """
        if not h2_cd:
            return ""

        return self.hcode_dict[h2_cd]["통계청 시도코드"]

    def get_kostat_h2_cd(self, h2_cd):
        """
        주어진 시군구코드(h2_cd)에 해당하는 통계청 시군구코드를 반환합니다.
        h2_cd가 None이거나 빈 문자열일 경우 빈 문자열을 반환합니다.

        :param h2_cd: 시군구코드
        :return: 통계청 시군구코드
        """
        if not h2_cd:
            return ""

        return self.hcode_dict[h2_cd]["통계청 시군구코드"]
