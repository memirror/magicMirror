# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/6/2

import unittest

from magicmirror.tools.es import esq
from magicmirror.tools.db import Question


class TestElasticSearchQuestion(unittest.TestCase):

    def setUp(self) -> None:
        self.questions = Question.query.with_entities(Question.question).limit(10)

    def test_es_is_on(self):
        self.assertIs(esq.ping(), True)

    def test_question_exist_in_es(self):
        for question, in self.questions:
            rs = esq.search(question, size=1)
            self.assertEqual(question, rs[0]["question"])

    def test_question_num_exist_in_es(self):
        for question, in self.questions:
            rs = esq.search(question, size=10)
            self.assertLessEqual(len(rs), 10)
            rs = esq.search(question, size=5)
            self.assertLessEqual(len(rs), 5)


if __name__ == '__main__':

    unittest.main()
 
