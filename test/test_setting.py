# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/27

import unittest

from magicmirror.setting import BAIDU_DEFAULT_HEADERS, SOGOU_DEFAULT_HEADERS, DB_MYSQL_URL


class TestSetting(unittest.TestCase):
    def test_headers(self):
        self.assertIn("Accept", BAIDU_DEFAULT_HEADERS)
        self.assertIn("Accept", SOGOU_DEFAULT_HEADERS)

    def test_url(self):
        self.assertIn("mysql", DB_MYSQL_URL)


if __name__ == '__main__':

    unittest.main()
