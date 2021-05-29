# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/27

import unittest

from magicmirror.realtimespider import baidu, sogou


class TestRealtimespider(unittest.TestCase):
    
    def test_baidu(self):
        out = baidu.BaiduApi("南京天气")()
        self.assertIsNotNone(out)

    def test_sogou(self):
        out = sogou.SogouApi("北京天气")()
        self.assertIsNotNone(out)


if __name__ == '__main__':

    unittest.main()
