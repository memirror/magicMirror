# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/27

from urllib import parse

from .base import BaseApi, get_headers
from ..setting import BAIDU_DEFAULT_HEADERS


class BaiduApi(BaseApi):

    url = "http://www.baidu.com/s?"

    def __init__(self, question: str, headers: dict = None):
        """
        :param question: 提问
        :param headers: http headers详情
        """
        super().__init__(question)
        if headers is None:
            headers = get_headers(BAIDU_DEFAULT_HEADERS)
        self.set_url(self.__class__.url + parse.urlencode([("w", self.question)]))
        self.set_headers(headers)

    def preprocess(self):
        # 百度图谱
        self.register("string(//div[@class='op_exactqa_s_answer c-color-t'])",
                      "string(//p[@class='op_exactqa_s_abstract'])",
                      weight=100,
                      save="all",
                      )
        # 百度百科
        self.register("//div[@class='op_exactqa_s_answer']/text()",
                      "//p[@class='op_exactqa_s_abstract c-gap-top-small']/span/text()",
                      weight=95,
                      save="all")
        # 百度百科
        self.register("string(//span[contains(text(), 'https://baike.baidu.com/')]/parent::p/parent::div)",
                      weight=74,
                      save="all",
                      )
        # 百度天气
        self.register("//p[@class='op_weather4_twoicon_temp']/text()",
                      [
                          "//p[@class='op_weather4_twoicon_weath']/text()",
                          "//p[@class='op_weather4_twoicon_wind']/text()"
                      ],
                      weight=90,
                      save="first")
        # 百度汉语
        self.register("string(//div[@class='op_exactqa_detail_s_answer']/span)",
                      "//a[@class='op_exactqa_detail_s_answer_showall c-gray OP_LOG_BTN']/@content",
                      weight=85,
                      save="all")
        # 百度汉语
        self.register("//div[@class='op_exactqa_detail_s_answer_scroll']//div/text()",
                      weight=84,
                      save="all")
        # 百度汉语
        self.register("//span[@class='op_dict_text2 op-dict3-gray']/text()",
                      weight=83,
                      save="all")

        # 百度医药
        self.register("//div[@class='c-abstract wenda-abstract-abstract']//span[2]/text()",
                      weight=80,
                      save="all")
        # 百度翻译
        self.register("//span[@class='op_dict_text2']/text()",
                      weight=70,
                      save="first")

        return self
     
