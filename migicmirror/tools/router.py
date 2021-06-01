# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/6/1

import abc
from typing import Generator


class Router(abc.ABC):

    def process(self, source: str = None) -> Generator:
        pass


class RouterByWeight(Router):

    apis: list = None

    def process(self, source: str = None):
        for api in self.apis:
            yield {
                "api": api.api,
                "source": api.source,
            }


class RouterBySource(Router):
    apidict: dict = None

    def process(self, source: str = None):
        yield {
            "api": self.apidict.get(source),
            "source": source,
        }
  
