import csv

"""
reverse geocoding은 도로명주소를 건물도형(shp)을 통해 추출하는 방식이다.
건물도형(shp)은 코드 값만 가지고 있기 때문에 코드를 도로명주소로 변환하는 작업이 필요하다.

shp 객체의 속성 값 예:
    ADR_MNG_NO: 11560132415473400000400004
    SIG_CD: 11560
    RN_CD: 4154734
    BULD_SE_CD: 0
    BULD_MNNM: 4
    BULD_SLNO: 4
    BUL_MAN_NO: 35552
    EQB_MAN_SN: 0
    EFFECT_DE: 20170427

코드에서 도로명주소로 변환하는 작업을 수행하는 클래스이다.
참조 데이터는 db/code/TN_SPRD_RDNM.txt 이다. 다운로드: https://business.juso.go.kr/addrlink/attrbDBDwld/attrbDBDwldList.do?cPath=99MD&menu=도로명

TN_SPRD_RDNM.txt 예시:
    48250|4805185|00|김해대로2325번길|Gimhae-daero 2325beon-gil|경상남도|김해시|2|||0|김해대로의 시작지점부터 약 23250m(기초번호 2325번) 지점에서 왼쪽으로 분기되는 길|||Gyeongsangnam-do|Gimhae-si||1|46|20091008|
    48250|4805187|01|김해대로2371번길|Gimhae-daero 2371beon-gil|경상남도|김해시|1|103|부원동|0|김해대로의 시작지점부터 약 23710m(기초번호 2371번) 지점에서 왼쪽으로 분기되는 길|||Gyeongsangnam-do|Gimhae-si|Buwon-dong|1|30|20091008|
    48250|4805188|01|김해대로2385번길|Gimhae-daero 2385beon-gil|경상남도|김해시|1|103|부원동|0|김해대로의 시작지점부터 약 23850m(기초번호 2385번) 지점에서 왼쪽으로 분기되는 길|||Gyeongsangnam-do|Gimhae-si|Buwon-dong|1|48|20091008|
    48250|4805189|00|김해대로2415번길|Gimhae-daero 2415beon-gil|경상남도|김해시|2|||0|김해대로의 시작지점부터 약 24150m(기초번호 2415번) 지점에서 왼쪽으로 분기되는 길|||Gyeongsangnam-do|Gimhae-si||1|16|20091008|
    48250|4805190|00|김해대로2431번길|Gimhae-daero 2431beon-gil|경상남도|김해시|2|||0|김해대로의 시작지점부터 약 24310m(기초번호 2431번) 지점에서 왼쪽으로 분기되는 길|||Gyeongsangnam-do|Gimhae-si||1|34|20091008|

컬럼 설명:
*   1    시군구코드     5           문자 PK1
*   2    도로명번호     7           문자 도로명코드 : 시군구코드(5) + 도로명번호(7)
    3    읍면동일련번호 2           문자 PK2
*   4    도로명         80          문자
    5    영문도로명     80          문자
*   6    시도명         40           문자
*   7    시군구명       40           문자
    8    읍면동구분     1           문자 0: 읍면, 1:동, 2:미부여
    9    읍면동코드     3           문자 법정동기준읍면동코드
    10   읍면동명       40           문자
    11   사용여부       1           문자 0: 사용, 1: 미사용
    12   부여사유       254         문자
    13   변경이력사유   1           문자     {0: 도로명변경, 1: 도로명폐지, 2: 시도시군구변경, 3: 읍면동변경, 4: 영문도로명변경, 9: 기타}
    14   변경이력정보   14           문자 도로명코드(12)+ 읍면동일련번호(2)     ※ 신규정보일경우“신규”로표시
    15   영문시도명     40           문자
    16   영문시군구명   40           문자
    17   영문읍면동명   40           문자
    18   도로구간의 시작 지점 기초번호  10 문자
    19   도로구간 끝지점 기초번호       10 문자
    20   효력발생일     8           문자 효력발생일자(YYYYMMDD)
    21   말소일자       8           문자 말소일자(YYYYMMDD)
"""


class RoadMatcher:
    # db/code/TN_SPRD_RDNM.txt 파일을 읽어와서 dict로 반환하는 클래스
    fieldnames = [
        "시군구코드",
        "도로명번호",
        "읍면동일련번호",
        "도로명",
        "영문도로명",
        "시도명",
        "시군구명",
        "읍면동구분",
        "읍면동코드",
        "읍면동명",
        "사용여부",
        "부여사유",
        "변경이력사유",
        "변경이력정보",
        "영문시도명",
        "영문시군구명",
        "영문읍면동명",
        "도로구간의 시작 지점 기초번호",
        "도로구간 끝지점 기초번호",
        "효력발생일",
        "말소일자",
    ]

    def __init__(self):
        filename = "db/code/TN_SPRD_RDNM.txt"
        self.road_dict = {}
        with open(filename, "r", encoding="cp949") as f:
            reader = csv.DictReader(f, delimiter="|", fieldnames=self.fieldnames)
            for row in reader:
                # 법정동코드,법정동명,폐지여부
                key = f"{row['시군구코드']}_{row['도로명번호']}"
                row["ADDR"] = f"{row['시도명']} {row['시군구명']} {row['도로명']}"
                self.road_dict[key] = row

    def get_road_name(self, pnu):
        # 1156013241 5473400000 400004
        # *       *       **     *
        # 0123456789 0123456789 012345

        key = f"{pnu[0:5]}_{pnu[8:15]}"
        return self.road_dict[key]["ADDR"]
