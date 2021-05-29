# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/27

import os
import unittest

from magicmirror.root import root


class TestRoot(unittest.TestCase):
    def test_root_equal(self):
        self.assertEqual(
            str(root), os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        )


if __name__ == '__main__':
    unittest.main()
