# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/6/1

import re
from functools import wraps
from typing import TypeVar, Callable, AnyStr

from fuzzywuzzy import fuzz


Number  = TypeVar("Number", int, float)
Compare = Callable[[AnyStr, AnyStr], Number]


def _rm_punctuation(seg: str) -> str:
    return re.sub(r"[^\w]", "", seg)


def preprocess(callback) -> Compare:
    @wraps(callback)
    def _(oq, sq):
        oq, sq = map(_rm_punctuation, [oq, sq])
        return callback(oq, sq)
    return _


token_sort_ratio = preprocess(fuzz.token_sort_ratio)
token_set_ratio  = preprocess(fuzz.token_set_ratio)
  
