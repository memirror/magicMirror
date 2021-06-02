# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/6/2

import unittest

from magicmirror.tools.whooshe import wq
from magicmirror.tools.db import Question


class TestElasticSearchQuestion(unittest.TestCase):

    def setUp(self) -> None:
        self.questions = Question.query.with_entities(Question.question).limit(3)


    def test_question_exist_in_es(self):
        for question, in self.questions:
            rs = wq.search(question, topk=1)
            self.assertEqual(question, rs[0]["question"])

    def test_question_num_exist_in_es(self):
        for question, in self.questions:
            rs = wq.search(question, topk=10)
            self.assertLessEqual(len(rs), 10)
            rs = wq.search(question, topk=5)
            self.assertLessEqual(len(rs), 5)


if __name__ == '__main__':

    unittest.main()
 
