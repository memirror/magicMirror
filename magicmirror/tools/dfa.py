# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/29

"""
DFA: 确定有限自动机
"""

class DFA:
    def __init__(self):
        self.d = {}
        self.end = "\x00"

    def preprocess(self, chars: str) -> str:
        return chars.lower()

    def add(self, chars: str) -> None:
        d = self.d
        chars = self.preprocess(chars)

        if not chars:
            return

        last = None
        for i, t in enumerate(chars):
            if i == len(chars) - 1:
                last[t] = {self.end: 0}
            else:
                if last is None:
                    last = d
                last = last.setdefault(t, {})

    def filter(self, msg: str, replace_by: str = "*") -> str:
        msg = self.preprocess(msg)
        ret = []
        start = 0
        while start < len(msg):
            location = 0
            d = self.d
            for char in msg[start:]:
                if char in d:
                    location += 1
                    if self.end not in d[char]:
                        d = d[char]
                    else:
                        ret.append(replace_by * location)
                        start += location - 1
                        break
                else:
                    ret.append(msg[start])
                    break
            else:
                ret.append(msg[start])

            start += 1
        return "".join(ret)

    def exist(self, msg: str) -> bool:
        msg = self.preprocess(msg)
        start = 0
        while start < len(msg):
            exist = 0
            d = self.d
            for char in msg[start:]:
                if char in d:
                    exist += 1
                    if self.end not in d[char]:
                        d = d[char]
                    else:
                        return True
            start += 1
        return False


def check_is_senstive(senstive_words=None) -> DFA:
    if senstive_words is None:
        senstive_words = []
    dfa = DFA()
    for word in senstive_words:
        dfa.add(word)
    return dfa
