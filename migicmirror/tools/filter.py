# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/6/1

import enum
import logging
from typing import Callable, List


logger = logging.getLogger("magicmirror.filter")


class Strategy(enum.Enum):

    strict = "strict"
    loose = "loose"


class Filter(object):
    def __init__(self, oq: str, sq: str):
        """
        :param oq: origin question
        :param sq: similary question
        """
        self.oq = oq
        self.sq = sq

    def will_drop(self) -> bool:
        return False


class NoFilter(Filter):
    """no filter"""


class SimpleFilter(Filter):

    strategy: Strategy = Strategy.strict
    callbacks: List[Callable[[str, str], float]] = [lambda oq, sq: 100.0]
    threshold: float = 80.0

    def will_drop(self) -> bool:
        for callback in self.callbacks:
            ratio = callback(self.oq, self.sq)
            logger.info("[oq] %s, [sq] %s, [similary ratio] %s, [threshold] %s",
                        self.oq, self.sq, ratio, self.threshold)
            if ratio < self.threshold:
                if self.strategy.value == "strict":
                    return True
            else:
                if self.strategy.value == "loose":
                    return False
        return False
