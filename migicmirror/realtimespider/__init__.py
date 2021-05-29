# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/27

import logging

from .baidu import BaiduApi
from .sogou import SogouApi


logger = logging.getLogger("magicmirror.realtimespider")

Apis = []

def register(api):
    Apis.append(api)

def realtimespider(question: str):
    for api in Apis:
        out = api(question)()
        if out:
            logger.info("[from] %s, [question] %s, [answer] %s", api.__name__, question, out)
            return out


register(BaiduApi)
register(SogouApi)
