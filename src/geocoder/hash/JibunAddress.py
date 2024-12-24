import re
from ..Tokenizer import Tokenizer
from ..tokens import *
from ..util.HSimplifier import HSimplifier


class JibunAddress:
    tokenizer = Tokenizer()
    hSimplifier = HSimplifier()

    re산n = re.compile(r"산\d+$")

    def hash(self, toks):
        """
        주어진 토큰 목록을 해시 문자열로 변환합니다.

        :param toks: 토큰 목록
        :return: 해시 문자열
        """
        h23 = ""
        hd = ""
        h5 = ""
        bng = ""

        length = len(toks)
        for n in range(length):
            tkn = toks.get(n)
            if tkn.t == TOKEN_H23 and h23 == "":
                h23 = self.hSimplifier.h23Hash(tkn.val)
            elif tkn.t == TOKEN_H4 and hd == "":
                hd = self.hSimplifier.h4Hash(tkn.val)
            elif tkn.t == TOKEN_RI and h5 == "":
                h5 = self.hSimplifier.h5Hash(tkn.val)
            elif tkn.t == TOKEN_BNG and bng == "":
                bng = self.__extractBng(tkn.val)
            else:
                continue
        # TOKEN_BLD       = 'BLD'
        # TOKEN_BLD_DONG  = 'BLD_DONG'

        bng = self.__bunjiHash(bng)
        hash = "{}_{}_{}_{}".format(h23, hd, h5, bng)
        return hash.replace("__", "_")

    def __safeExtract(self, reg, val):
        """
        정규 표현식을 사용하여 값에서 안전하게 문자열을 추출합니다.

        :param reg: 정규 표현식 객체
        :param val: 입력 값
        :return: 추출된 문자열 또는 None
        """
        m = reg.search(val)
        if m:
            return m.group()
        else:
            return None

    def __extractBng(self, val):
        """
        번지 값을 추출하고 형식을 변환합니다.

        :param val: 입력 값
        :return: 변환된 번지 값
        """
        # 1의2(번지)
        s = self.__safeExtract(self.tokenizer.re_bunjihead_n_의_n, val)
        if s:
            return s.replace("의", "-").replace("번지", "")

        # 1번지2호 => 1-2
        s = self.__safeExtract(self.tokenizer.re_bunjihead_번지_호, val)
        if s:
            return s.replace("번지", "-").replace("호", "")

        s = self.__safeExtract(self.tokenizer.re_bunjihead_n_n_bng, val)
        if s:
            return s.replace("번지", "")

        # '1013-6호'
        s = self.__safeExtract(self.tokenizer.re_bunjihead_n_n_호, val)
        if s:
            return s.replace("호", "")

        # 1번지 => 1-0
        s = self.__safeExtract(self.tokenizer.re_bunjihead_n_번지, val)
        if s:
            return s.replace("번지", "") + "-0"

        # 6호   => 6-0
        s = self.__safeExtract(self.tokenizer.re_bunjihead_n_호, val)
        if s:
            return s.replace("호", "") + "-0"

        return val

    def __bunjiHash(self, no1):
        """
        번지 문자열을 해시 문자열로 변환합니다.

        :param no1: 번지 문자열
        :return: 0-0 형식의 해시 문자열
        """
        if no1.isdigit() or self.re산n.match(no1):  # r'산\d+$'
            return no1 + "-0"

        # 1-2(번지)
        if self.tokenizer.re_bunji_n_n_bng.match(no1):  # r'^\d+-\d+(번지)?$'
            return no1.replace("번지", "")

        # 1의2(번지)
        if self.tokenizer.re_bunji_n_의_n.match(no1):  # r'^\d+의\d+(번지)?$'
            return no1.replace("의", "-").replace("번지", "")

        #  1번지2(호)
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
