# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/6/2

import time
import unittest

from magicmirror.tools.limit import calllimit


class TestLimit(unittest.TestCase):

    def execute(self, sleep_seconds: int):
        time.sleep(sleep_seconds)
        return "success"

    async def aexecute(self, sleep_seconds: int):
        return self.execute(sleep_seconds)

    def test_limitexecuteduration(self):
        self.assertLessEqual(
            calllimit.LimitExecuteDuration(1).run(self.execute, 0.9)._result,
            "success")
        self.assertIsNone(
            calllimit.LimitExecuteDuration(1).run(self.execute, 2)._result
        )


if __name__ == '__main__':

    unittest.main()
 
