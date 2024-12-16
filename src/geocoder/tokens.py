from typing import List

TOKEN_UNKNOWN = "UNKNOWN"
TOKEN_H1 = "H1"
TOKEN_H23 = "H23"
TOKEN_H4 = "H4"
TOKEN_RI = "RI"
TOKEN_ROAD = "ROAD"
TOKEN_UNDER = "지하"
TOKEN_SAN = "산"
TOKEN_BNG = "번지"
TOKEN_BLDNO = "건번"
TOKEN_BLD = "BLD"
TOKEN_BLD_DONG = "BLD_DONG"
TOKEN_FLOOR = "FLOOR"
TOKEN_BLD_HO = "BLD_HO"
TOKEN_NUMERIC = "NUMERIC"
TOKEN_COMMA = "COMMA"
TOKEN_EXTRA = "EXTRA"


class Token:
    """
    Token 클래스는 문자열 값과 토큰 유형을 나타내는 객체를 생성합니다.

    속성:
        val (str): 토큰의 문자열 값.
        t (int): 토큰의 유형. 기본값은 TOKEN_UNKNOWN.

    메서드:
        __init__(self, v, t=TOKEN_UNKNOWN):
            Token 객체를 초기화합니다.
            매개변수:
                v (str): 토큰의 문자열 값.
                t (int): 토큰의 유형. 기본값은 TOKEN_UNKNOWN.

        __repr__(self):
            Token 객체를 문자열로 표현합니다.
            반환값:
                str: 토큰의 문자열 값과 유형을 포함한 문자열.
    """

    val = ""
    t = TOKEN_UNKNOWN

    def __init__(self, v, t=TOKEN_UNKNOWN):
        self.val = v
        self.t = t

    def __repr__(self):
        return f"{self.val} ({self.t})"


class Tokens:
    """
    Tokens 클래스는 문자열 토큰을 관리하는 여러 메서드를 제공합니다.

    속성:
        toks (List[Token]): Token 객체의 리스트.

    메서드:
        __init__(self, toks):
            주어진 문자열 리스트에서 빈 문자열을 제거하고 Token 객체로 변환하여 초기화합니다.

        __len__(self):
            Token 리스트의 길이를 반환합니다.

        __getitem__(self, position):
            주어진 위치의 Token 값을 반환합니다.

        get(self, position):
            주어진 위치의 Token 객체를 반환합니다.

        prev(self, position):
            주어진 위치의 이전 Token 객체를 반환합니다. 위치가 0이면 빈 Token 객체를 반환합니다.

        isBracketEnd(self, pos):
            주어진 위치의 Token 값이 ")"로 끝나는지 확인합니다.

        isBracketBegin(self, pos):
            주어진 위치의 Token 값이 "("로 시작하는지 확인합니다.

        index(self, t: str, begin=0) -> bool:
            주어진 문자열 t가 Token 리스트에서 처음으로 나타나는 위치를 반환합니다. 찾지 못하면 -1을 반환합니다.

        lastIndex(self, t):
            주어진 문자열 t가 Token 리스트에서 마지막으로 나타나는 위치를 반환합니다. 찾지 못하면 -1을 반환합니다.

        merge(self, begin, end, t=TOKEN_EXTRA, sep=" "):
            주어진 범위의 Token 값을 하나의 Token으로 병합합니다.

        split(self, pos, splitpos, t1, t2):
            주어진 위치의 Token 값을 두 개의 Token으로 분할합니다.

        delete(self, pos):
            주어진 위치의 Token을 삭제합니다.

        searchTypeSequence(self, fromSeq):
            주어진 Token 타입 시퀀스를 검색하여 시작과 끝 위치를 반환합니다.

        changeTypeSequence(self, begin, toTypeSeq):
            주어진 위치에서 시작하여 Token 타입 시퀀스를 변경합니다.

        __repr__(self):
            Token 값들을 "|"로 구분하여 문자열로 반환합니다.

        hasTypes(self, t):
            주어진 Token 타입이 리스트에 존재하는지 확인합니다.
    """

    toks = []  # type: List[Token]

    def __init__(self, toks):
        # 빈 토큰 제거
        self.toks = [Token(t, TOKEN_UNKNOWN) for t in toks if t != ""]

    def __len__(self):
        return len(self.toks)

    def __getitem__(self, position):
        return self.toks[position].val

    def get(self, position):
        return self.toks[position]

    def prev(self, position):
        if position == 0:
            return Token("", TOKEN_UNKNOWN)
        return self.toks[position - 1]

    def isBracketEnd(self, pos):
        return self.toks[pos].val.endswith(")")

    def isBracketBegin(self, pos):
        return self.toks[pos].val.startswith("(")

    def index(self, t: str, begin=0) -> bool:
        length = len(self.toks)
        for pos in range(begin, length):
            o = self.toks[pos]
            if o.t == t:
                return pos
            pos += 1

        return -1

    def lastIndex(self, t):
        pos = len(self.toks) - 1
        for o in self.toks[::-1]:  # reverse
            if o.t == t:
                return pos
            pos -= 1

        return -1

    def merge(self, begin, end, t=TOKEN_EXTRA, sep=" "):
        if t == None:
            t = TOKEN_UNKNOWN

        val = ""
        seperator = ""
        for n in range(begin, end):
            val += seperator + self.toks[n].val
            seperator = sep

        del self.toks[begin:end]
        self.toks.insert(begin, Token(val, t))

    def split(self, pos, splitpos, t1, t2):
        s = self.toks[pos].val
        del self.toks[pos]
        if s[splitpos:]:
            self.toks.insert(pos, Token(s[splitpos:], t2))
        self.toks.insert(pos, Token(s[0:splitpos], t1))

    def delete(self, pos):
        del self.toks[pos]

    def searchTypeSequence(self, fromSeq):
        """Token Type sequence 찾기
        결과 begin, end 리턴
        """

        begin = -1
        end = -1
        seq0 = fromSeq[0]
        seqLen = len(fromSeq)
        pos = 0
        for pos in range(len(self.toks)):
            if self.toks[pos].t == seq0:
                found = True
                for n in range(1, seqLen):
                    if len(self.toks) <= pos + n or fromSeq[n] != self.toks[pos + n].t:
                        found = False
                        break
                if found:
                    begin = pos
                    end = begin + seqLen
                    break

        return begin, end

    def changeTypeSequence(self, begin, toTypeSeq):
        """type 변경
        begin: 시작 position
        toSeq: 새 Token Type sequence
        """
        for n in range(len(toTypeSeq)):
            self.toks[n + begin].t = toTypeSeq[n]

    def __repr__(self):
        vals = []
        for tkn in self.toks:
            vals.append(tkn.val)

        return "|".join(vals)

    def hasTypes(self, t):
        for tkn in self.toks:
            if tkn.t == t:
                return True

        return False
