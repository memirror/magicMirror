# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/6/1

from limits import storage
from limits import strategies
from limits import parse


"""
https://limits.readthedocs.io/en/stable/index.html
"""


class MemoryRateLimit(object):

    storage = storage.MemoryStorage()
    window = strategies.MovingWindowRateLimiter(storage)
    rate = parse("1/second")

    def __init__(self, identifier: str):
        self.identifier = identifier

    def allow(self):
        return self.window.hit(self.rate, self.identifier)
