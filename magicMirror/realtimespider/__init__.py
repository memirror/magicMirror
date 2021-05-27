# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/27

from .baidu import BaiduApi
from .sogou import SogouApi


Apis = []

def register(api):
    Apis.append(api)

def realtimespider(question: str):
    for api in Apis:
        out = api(question)()
        if out:
            return out


register(BaiduApi)
register(SogouApi)
