# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/27

from abc import ABC
from bisect import insort
from operator import itemgetter
from typing import Union

import requests
from lxml.etree import HTML


def get_headers(headers: str) -> dict:
    response = {}
    for header in headers.split("\n"):
        if not header.strip():
            continue
        k, v = header.split(":", maxsplit=1)
        k, v = k.strip(), v.strip()
        response[k] = v
    return response


class BaseApi(object):

    def __init__(self, question: str):
        self.question = question

        # 防止权重相同时无法排序
        self._count = 0
        # 默认超时
        self._default_timeout = 2.0
        # 存储所需配置
        self._params = {}
        # 按权重存储问答xpath表达式
        self._regex = []

    def __call__(self):
        return self.preprocess().process()

    def set(self, key, value):
        self._params[key] = value
        return self

    def get(self, key):
        return self._params.get(key)

    def set_url(self, url):
        return self.set("url", url)

    def set_headers(self, headers):
        return self.set("headers", headers)

    def set_params(self, params):
        return self.set("params", params)

    def set_timeout(self, timeout):
        return self.set("timeout", timeout)

    def set_proxies(self, proxies):
        return self.set("proxies", proxies)

    def response(self):
        response = requests.get(
            self.get("url"),
            data=self.get("data"),
            params=self.get("params"),
            headers=self.get("headers"),
            cookies=self.get("cookies"),
            timeout=self.get("timeout") or self._default_timeout,
            proxies=self.get("proxies"),
        )
        if response.status_code == 200:
            return HTML(response.text)

    def preprocess(self):
        raise NotImplemented()

        def process(self):
        response = self.response()
        ret = {}
        if not len(response):
            return
        for need in self._regex:
            result_regex      = need.retregex
            description_regex = need.descregex
            save              = need.save
            result = response.xpath(result_regex)
            all_description = []
            if not result:
                continue
            for per_description_regex in description_regex:
                description = response.xpath(per_description_regex)
                if not description:
                    continue
                all_description.append(description)

            if isinstance(result, str):
                result = [result]

            _all_description = []
            for description in all_description:
                if isinstance(description, str):
                    description = [description]
                for i, desc in enumerate(description):
                    description[i] = re.sub(r"\s", "", desc, flags=re.M | re.A)
                _all_description.append(description)
            all_description = _all_description

            for i, _ in enumerate(result):
                result[i] = re.sub(r"\s", "", result[i], flags=re.M | re.A)

            if save == "first":
                result = result[0]
                description = all_description[0][0]
            else:
                result = ", ".join(result)
                description = ", ".join([obj for description in all_description for obj in description ])

            ret["result"] = result
            ret["desc"] = description

            return ret

    def register(self,
                 result_regex: str,
                 description_regex: Union[str, list] = None,
                 weight: int = 0,
                 save: str = "first"
                 ):
        """
        :param result_regex: 结果提取xpath格式
        :param description_regex: 结果详情xpath格式
        :param weight: 权重
        :param save:   结果详情截取方式
                            --first 只保留第一个
                            --all 保留所有
        :return:
        """
        saves = ("first", "all")
        assert save in saves, "just support '{}'".format(", ".join(saves))
        if description_regex is None:
            description_regex = []
        elif isinstance(description_regex, str):
            description_regex = [description_regex]
        insort(self._regex, p((-weight, self._count, result_regex, description_regex, save)))
        self._count += 1


class p(tuple):
    weight    = property(itemgetter(0))
    autocount = property(itemgetter(1))
    retregex  = property(itemgetter(2))
    descregex = property(itemgetter(3))
    save      = property(itemgetter(4))
