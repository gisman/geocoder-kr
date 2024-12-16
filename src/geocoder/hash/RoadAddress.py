import re
from ..Tokenizer import Tokenizer
from ..tokens import *
from ..util.HSimplifier import HSimplifier
from ..util.RoadSimplifier import RoadSimplifier


class RoadAddress:
    tokenizer = Tokenizer()
    hSimplifier = HSimplifier()
    roadSimplifier = RoadSimplifier()

    def hash(self, toks):
        """
        주어진 토큰 목록을 해시 문자열로 변환합니다.

        :param toks: 토큰 목록
        :return: 해시 문자열
        """
        h23 = ""
        road = ""
        no1 = ""
        under = ""
        road_pos = -1

        length = len(toks)
        for n in range(length):
            tkn = toks.get(n)
            if tkn.t == TOKEN_H23 and h23 == "":
                h23 = self.hSimplifier.h23Hash(tkn.val)
            elif tkn.t == TOKEN_ROAD and road == "":
                road = self.roadSimplifier.roadHash(tkn.val)
                road_pos = n
            elif tkn.t == TOKEN_BLDNO and no1 == "":
                no1 = tkn.val
            elif tkn.t == TOKEN_UNDER and no1 == "":
                under = tkn.val
            else:
                continue
        # TOKEN_BLD       = 'BLD'
        # TOKEN_BLD_DONG  = 'BLD_DONG'
        # if not h23:
        #     h23 = toks.
        if h23.startswith("세종"):
            h23 = "세종시"

        if no1.isdigit():
            no1 = no1 + "-0"
        else:
            no1 = self.__bunjiHash(no1)

        # h23 판단 불가
        if road_pos > 0 and h23 == "":
            h23_pos = road_pos - 1
            h23 = self.hSimplifier.h23Hash(toks.get(h23_pos).val)
            if h23.endswith(("읍", "면", "동")) and h23_pos > 0:
                h23 = self.hSimplifier.h23Hash(toks.get(h23_pos - 1).val)

        s = "{}_{}_{}_{}".format(h23, road, under, no1)
        return s.replace("__", "_")

    def __hasH3(self, toks):
        """
        주어진 토큰 목록에 H3 토큰이 있는지 확인합니다.

        :param toks: 토큰 목록
        :return: H3 토큰 존재 여부
        """
        return self.tokenizer.hasH3(toks)

    def __bunjiHash(self, no1):
        """
        번지 번호를 해시 문자열로 변환합니다.

        :param no1: 번지 번호
        :return: 해시 문자열
        """
        if no1.isdigit() or no1.startswith("산"):
            return no1 + "-0"

        # 1-2번지 => 1-2
        # 1-2 => 1-2
        if self.tokenizer.re_bunji_n_n_bng.match(no1):  # r'^\d+-\d+(번지)?$'
            return no1.replace("번지", "")

        if self.tokenizer.re_bunji_n_의_n.match(no1):  # r'^\d+의\d+(번지)?$'
            return no1.replace("의", "-").replace("번지", "")

        # 1번지2호 => 1-2
        if self.tokenizer.re_bunji_번지_호.match(no1):  # r'^\d+번지\d+(호)?$'
            return no1.replace("번지", "-").replace("호", "")

        # '1013-6호'
        if self.tokenizer.re_bunji_n_n_호.match(no1):  # r'^\d+-\d+호$'
            return no1.replace("호", "")

        # 1번지 => 1-0
        if self.tokenizer.re_bunji_n_번지.match(no1):  # r'^\d+번지$'):
            return no1.replace("번지", "") + "-0"

        # 6호   => 6-0
        if self.tokenizer.re_bunji_n_호.match(no1):  # r'^\d+호$'):
            return no1.replace("호", "") + "-0"

        return ""
