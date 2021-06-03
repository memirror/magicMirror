# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/27

import os
import logging
import random
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


def random_answer_by_question_id(question_id):
    answers = Answer.query.filter_by(question_id=question_id).all()
    answers = set([answer.answer for answer in answers])
    return random.choice(list(answers))


def qwsearch(question: str) -> Union[str]:
    for obj in wq.search(question):
        if SimpleFilter(question, obj["question"]).will_drop():
            continue
        return random_answer_by_question_id(obj["id"])


def qessearch(question: str) -> Union[str]:
    for obj in esq.search(question):
        if SimpleFilter(question, obj["question"]).will_drop():
            continue
        return random_answer_by_question_id(obj["id"])


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

if os.environ.get("MM_ELASTICSEARCH_SUPPORT", "true") == "true" and esq.ping():
    register(qessearch, "elasticsearch", 2000)
else:
    os.environ["MM_ELASTICSEARCH_SUPPORT"] = "false"
