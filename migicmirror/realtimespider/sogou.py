# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/27

from urllib import parse

from .base import BaseApi, get_headers
from ..setting import SOGOU_DEFAULT_HEADERS


class SogouApi(BaseApi):

    url = "http://www.sogou.com/web?"

    def __init__(self, question: str, headers: dict = None):
        """
        :param question: 提问
        :param headers: http headers详情
        """
        super().__init__(question)
        if headers is None:
            headers = get_headers(SOGOU_DEFAULT_HEADERS)
        (
            self.set_url(
                        self.__class__.url
                        + parse.urlencode([("query", self.question)]))
                .set_headers(headers)
        )

    def preprocess(self):

        # 搜狗天气
        self.register(
            "string(//div[@class='w-desc currentDay'])",
            weight=100,
            save="all"
        )

        # 搜狗百科
        self.register(
            "//p[@class='title-summary ']/text()",
            [
                "//p[@class='star-wiki space-txt']/text()",
                "//p[@class='star-wiki ']/text()",
            ],
            weight=99,
            save="all",
        )
        return self
