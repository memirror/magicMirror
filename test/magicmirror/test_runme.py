# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/6/2

import unittest
import time

from magicmirror import runme
from magicmirror.tools.cache import SimpleCache
from magicmirror.tools.db import Question, Answer


class TestMM(unittest.TestCase):
    def setUp(self) -> None:
        self.fake_insert = False
        self.old_cache = runme.mm.cache
        if not Question.query.filter_by(question="你叫啥").first():
            q = Question(question="你叫啥").create()
            a = Answer(answer="我是魔镜, 无所不知的魔镜")
            q.answers.append(a)
            q.save()
            self.fake_insert = True
        
    def test_not_from_cache(self):
        runme.mm.cache = SimpleCache(threshold=10, default_timeout=1)
        runme.mm("你叫啥")
        time.sleep(2)
        self.assertNotIn(
            "cache",
            runme.mm("你叫啥")["source"]
        )

    def test_from_cache(self):
        runme.mm.cache = SimpleCache(threshold=1, default_timeout=5)
        runme.mm("你叫啥")
        self.assertIn(
            "cache",
            runme.mm("你叫啥")["source"]
        )

    def tearDown(self) -> None:
        runme.mm.cache = self.old_cache

        if self.fake_insert:
            Question.query.filter_by(question="你叫啥").first().delete()


if __name__ == '__main__':

    unittest.main()
 
