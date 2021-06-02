# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/27

import logging
from typing import List, Dict, Any, Callable, Union
from bisect import insort

from .realtimespider import BaiduApi, SogouApi
from .tools.whooshe import wq
from .tools.db import Answer
from .tools.es import esq
from .tools.filter import SimpleFilter
from .tools import similary


Api: Callable[[str], str] = None
Apis: List[tuple] = []
ApiDict: Dict[str, Api] = {}

logger = logging.getLogger("magicmirror")


SimpleFilter.callbacks = [
    similary.token_set_ratio, similary.token_sort_ratio,
]


def qwsearch(question: str) -> Union[str]:
    for obj in wq.search(question):
        if SimpleFilter(question, obj["question"]).will_drop():
            continue
        answer = Answer.query.filter_by(question_id=obj["id"]).first()
        return answer.answer if answer else None


def qessearch(question: str) -> Union[str]:
    for obj in esq.search(question):
        if SimpleFilter(question, obj["question"]).will_drop():
            continue
        answer = Answer.query.filter_by(question_id=obj["id"]).first()
        return answer.answer if answer else None


class p(tuple):
    weight = property(lambda self: self[0])
    api = property(lambda self: self[1])
    source = property(lambda self: self[2])
    others = property(lambda self: self[3:])


def register(api: callable, source: str, weight, **kwargs):
    ApiDict[source] = api
    insort(Apis, p((-weight, api, source, kwargs)))


register(lambda q: BaiduApi(q)(), "baidu", 900)
register(lambda q: SogouApi(q)(), "sogou", 800)
register(qwsearch, "whoosh", 1000)
register(qessearch, "elasticsearch", 2000)
