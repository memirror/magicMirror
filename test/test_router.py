# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/6/1

import unittest

from magicmirror import Apis, ApiDict
from magicmirror.tools.router import RouterByWeight, RouterBySource


class TestRouterByWeight(unittest.TestCase):
    
    def setUp(self) -> None:
        router = RouterByWeight
        router.apis = Apis
        self.router = router

    def test_router(self) -> None:
        hope_order = [api.source for api in Apis]
        real_order = []
        for d in self.router().process():
            source = d["source"]
            real_order.append(source)
        self.assertEqual(hope_order, real_order)

    def tearDown(self) -> None:
        RouterByWeight.apis = None


class TestRouterBySource(unittest.TestCase):

    def setUp(self) -> None:
        router = RouterBySource
        router.apidict = ApiDict
        self.router = router

    def test_router(self) -> None:
        for d in self.router().process("baidu"):
            self.assertEqual("baidu", d["source"])
            self.assertEqual(ApiDict["baidu"], d["api"])
        for d in self.router().process("sogou"):
            self.assertEqual("sogou", d["source"])
            self.assertEqual(ApiDict["sogou"], d["api"])

    def tearDown(self) -> None:
        RouterBySource.apidict = None


if __name__ == '__main__':

    unittest.main()


