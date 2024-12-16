# python 3
# -*- coding: utf-8 -*-

import re
import csv
import json
from .Tokenizer import Tokenizer
from .tokens import *
from .hash.JibunAddress import JibunAddress
from .hash.BldAddress import BldAddress
from .hash.RoadAddress import RoadAddress
from .util.HSimplifier import HSimplifier
from .util.hcodematcher import HCodeMatcher


class Geocoder:
    """
    Geocoder 클래스는 주소를 해시하고 검색하는 기능을 제공합니다.

    속성:
        tokenizer (Tokenizer): 주소를 토큰화하는 객체.
        jibunAddress (JibunAddress): 지번 주소 해시 객체.
        bldAddress (BldAddress): 건물 주소 해시 객체.
        roadAddress (RoadAddress): 도로명 주소 해시 객체.
        hsimplifier (HSimplifier): 주소 단순화 객체.
        hcodeMatcher (HCodeMatcher): 행정 코드 매칭 객체.

    메서드:
        __init__(self, db):
            Geocoder 객체를 초기화합니다.

        __classfy(self, toks):
            주소 토큰을 분류하여 주소 유형을 반환합니다.

        __bldAddressHash(self, toks):
            건물 주소 해시를 반환합니다.

        __jibunAddressHash(self, toks):
            지번 주소 해시를 반환합니다.

        __roadAddressHash(self, toks):
            도로명 주소 해시를 반환합니다.

        addressHash(self, addr):
            주소를 해시하고 관련 정보를 반환합니다.

        search(self, addr):
            주소를 검색하고 결과를 반환합니다.

        get_h1(self, val):
            주소의 h1 코드를 반환합니다.

        get_h2(self, val):
            주소의 h2 코드를 반환합니다.

        most_similar_address(self, toks, key):
            가장 유사한 주소를 검색하여 반환합니다.
    """

    tokenizer = Tokenizer()
    jibunAddress = JibunAddress()
    bldAddress = BldAddress()
    roadAddress = RoadAddress()
    hsimplifier = HSimplifier()
    hcodeMatcher = HCodeMatcher()

    def __init__(self, db):
        self.db = db

        self.NOT_ADDRESS = "NOT_ADDRESS"
        self.JIBUN_ADDRESS = "JIBUN_ADDRESS"
        self.BLD_ADDRESS = "BLD_ADDRESS"
        self.ROAD_ADDRESS = "ROAD_ADDRESS"
        self.UNRECOGNIZABLE_ADDRESS = "UNRECOGNIZABLE_ADDRESS"

    def __classfy(self, toks):
        """
        주소 토큰을 분류하여 주소 유형을 반환합니다.

        Args:
            toks (Tokens): 주소를 구성하는 토큰 객체.

        Returns:
            str: 주소 유형을 나타내는 문자열. 가능한 값은 다음과 같습니다:
                - self.NOT_ADDRESS: 주소가 아닌 경우.
                - self.ROAD_ADDRESS: 도로명 주소인 경우.
                - self.JIBUN_ADDRESS: 지번 주소인 경우.
                - self.BLD_ADDRESS: 건물 주소인 경우.
                - self.UNRECOGNIZABLE_ADDRESS: 인식할 수 없는 주소인 경우.
        """
        if len(toks) < 3:
            return self.NOT_ADDRESS

        if toks.hasTypes(TOKEN_ROAD) and toks.hasTypes(TOKEN_BLDNO):
            return self.ROAD_ADDRESS

        if toks.hasTypes(TOKEN_BNG):
            return self.JIBUN_ADDRESS

        if toks.hasTypes(TOKEN_BLD):
            return self.BLD_ADDRESS

        return self.UNRECOGNIZABLE_ADDRESS

    def __bldAddressHash(self, toks):
        """
        주어진 토큰을 사용하여 주소 해시를 생성합니다.

        Args:
            toks (list): 주소 해시에 사용될 토큰 리스트.

        Returns:
            str: 생성된 주소 해시.
        """
        return self.bldAddress.hash(toks)

    def __jibunAddressHash(self, toks):
        """
        주어진 토큰을 사용하여 지번 주소의 해시 값을 반환합니다.

        Args:
            toks (list): 해시 값을 생성하는 데 사용될 토큰들의 리스트.

        Returns:
            str: 지번 주소의 해시 값.
        """
        return self.jibunAddress.hash(toks)

    def __roadAddressHash(self, toks):
        """
        주어진 토큰(toks)을 사용하여 도로명 주소의 해시 값을 반환합니다.

        Args:
            toks (str): 해시 값을 생성하는 데 사용될 토큰.

        Returns:
            int: 도로 주소의 해시 값.
        """
        return self.roadAddress.hash(toks)

    def addressHash(self, addr):
        """
        주어진 주소 문자열을 해시하고, 토큰화된 주소, 주소 유형, 오류 메시지를 반환합니다.

        Args:
            addr (str): 해시할 주소 문자열.

        Returns:
            tuple:
                - hash (str): 주소의 해시 값.
                - toks (list): 토큰화된 주소 리스트.
                - addressCls (int): 주소 유형을 나타내는 상수.
                - errmsg (str): 오류 메시지.

        오류 유형:
            - "NOT_ADDRESS ERROR": 주소로 인식되지 않는 경우.
            - "JIBUN HASH ERROR": 지번 주소 해시 오류.
            - "BLD HASH ERROR": 건물 주소 해시 오류.
            - "ROAD HASH ERROR": 도로명 주소 해시 오류.
            - "UNRECOGNIZABLE_ADDRESS ERROR": 인식할 수 없는 주소 오류.
            - "RUNTIME ERROR": 실행 중 발생한 오류.
        """
        hash = ""
        toks = []
        addressCls = self.NOT_ADDRESS
        errmsg = ""

        try:
            toks = self.tokenizer.tokenize(addr)
            addressCls = self.__classfy(toks)

            if addressCls == self.NOT_ADDRESS:
                hash = ""
                errmsg = "NOT_ADDRESS ERROR"
            elif addressCls == self.JIBUN_ADDRESS:
                hash = self.jibunAddress.hash(toks)
                if not hash:
                    errmsg = "JIBUN HASH ERROR"
            elif addressCls == self.BLD_ADDRESS:
                hash = self.bldAddress.hash(toks)
                if not hash:
                    errmsg = "BLD HASH ERROR"
            elif addressCls == self.ROAD_ADDRESS:
                hash = self.roadAddress.hash(toks)
                if not hash:
                    errmsg = "ROAD HASH ERROR"
            elif addressCls == self.UNRECOGNIZABLE_ADDRESS:
                hash = ""
                errmsg = "UNRECOGNIZABLE_ADDRESS ERROR"

        except:
            hash = ""
            errmsg = "RUNTIME ERROR"

        return hash, toks, addressCls, errmsg

    def search(self, addr):
        """
        주어진 주소를 검색하여 가장 유사한 주소 정보를 반환합니다.

        Parameters:
        addr (str): 검색할 주소 문자열.

        Returns:
        dict: 검색 결과를 포함한 딕셔너리. 성공 시, 딕셔너리는 다음 키를 포함합니다:
            - success (bool): 검색 성공 여부.
            - errmsg (str): 오류 메시지 (성공 시 빈 문자열).
            - h1_cd (str): h1 코드 (성공 시).
            - h2_cd (str): h2 코드 (성공 시).
            - kostat_h1_cd (str): KOSTAT h1 코드 (성공 시).
            - kostat_h2_cd (str): KOSTAT h2 코드 (성공 시).
            - hash (str): 주소 해시 값.
            - address (str): 입력된 주소.
            - addressCls (str): 주소 클래스.
            - toksString (str): 토큰 문자열.

        오류가 발생하거나 주소를 찾을 수 없는 경우, 딕셔너리는 다음 키를 포함합니다:
            - success (bool): False.
            - errmsg (str): 오류 메시지.
            - hash (str): 주소 해시 값.
            - address (str): 입력된 주소.
            - addressCls (str): 주소 클래스.
            - toksString (str): 토큰 문자열.
        """
        hash = ""
        toks = []
        addressCls = self.NOT_ADDRESS
        errmsg = "RUNTIME ERROR"

        if not isinstance(addr, str):
            return None

        address = addr.strip('"')
        if address == "":
            addressCls = self.NOT_ADDRESS
            return None

        hash, toks, addressCls, errmsg = self.addressHash(address)
        toksString = self.tokenizer.getToksString(toks)

        if hash:
            val = self.most_similar_address(toks, hash)
            if not val:
                val = {"success": False, "errmsg": "NOTFOUND ERROR"}
            else:
                val["success"] = True
                val["errmsg"] = ""

                try:
                    h1_cd = self.get_h1(val)
                    h2_cd = self.get_h2(val)
                    val["h1_cd"] = h1_cd
                    val["h2_cd"] = h2_cd
                    val["kostat_h1_cd"] = self.hcodeMatcher.get_kostat_h1_cd(h2_cd)
                    val["kostat_h2_cd"] = self.hcodeMatcher.get_kostat_h2_cd(h2_cd)
                except Exception as e:
                    val["h1_cd"] = ""
                    val["h2_cd"] = ""
                    val["kostat_h1_cd"] = ""
                    val["kostat_h2_cd"] = ""
                    # print(e, address, val)
        else:
            val = {"success": False, "errmsg": errmsg}

        val["hash"] = hash
        val["address"] = address
        val["addressCls"] = addressCls
        val["toksString"] = toksString

        return val

    def get_h1(self, val):
        """
        주어진 값에서 특정 키의 h1 코드인 첫 두 문자를 반환합니다.

        Args:
            val (dict): 'hc', 'lc', 'bn' 키를 포함하는 딕셔너리.

        Returns:
            str: 'hc', 'lc', 'bn' 중 하나의 첫 두 문자.
                 해당 키가 존재하지 않으면 None을 반환합니다.
        """
        if val["hc"]:
            return val["hc"][:2]
        elif val["lc"]:
            return val["lc"][:2]
        elif val["bn"]:
            return val["bn"][:2]

    def get_h2(self, val):
        """
        주어진 값에서 h2 코드를 추출하여 반환합니다.

        Args:
            val (dict): 'hc', 'lc', 또는 'bn' 키를 포함하는 딕셔너리.

        Returns:
            str: h2 코드 문자열.

        Raises:
            KeyError: 'hc', 'lc', 또는 'bn' 키가 딕셔너리에 없을 경우.
        """
        if val["hc"]:
            h2_cd = val["hc"][:5]
        elif val["lc"]:
            h2_cd = val["lc"][:5]
        elif val["bn"]:
            h2_cd = val["bn"][:5]

        return self.hcodeMatcher.get_h2_cd(h2_cd)

    def most_similar_address(self, toks, key):
        """
        주어진 토큰과 키를 사용하여 가장 유사한 주소를 반환합니다.

        Args:
            toks (list): 주소를 나타내는 토큰 리스트.
            key (str): 데이터베이스에서 검색할 키.

        Returns:
            dict or None: 가장 유사한 주소를 나타내는 딕셔너리.
                  유사한 주소가 없거나 오류가 발생한 경우 None을 반환합니다.

        예외:
            Exception: 데이터베이스 접근 또는 JSON 파싱 중 오류가 발생할 수 있습니다.
        """
        try:
            o = self.db.get(key)
            if o == None:
                return None

            if isinstance(o, bytearray) or isinstance(o, bytes):
                d = json.loads(o)
            else:
                d = o

            # h1 다르면 배제
            i = toks.index(TOKEN_H1)
            if i > -1:
                h1 = self.hsimplifier.h1Hash(toks[i])
            else:
                h1 = None

            if h1 == None:
                return d[0]

            # 건물 번호 있으면 더 정확하다. 2024.05.10
            for r in d:
                if r["h1"] == h1 and r["bn"]:
                    return r

            for r in d:
                if r["h1"] == h1:
                    return r
            # 길이름 다르면 배제: 보류
            return
        except Exception as e:
            # print(e)
            return None
