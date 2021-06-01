# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/6/1

from elasticsearch import helpers

from .base import ElastciSearchCore
from ..db import Question


class ElasticSearchQuestion(ElastciSearchCore):

    def create(self):
        actions = []
        for obj in (Question.query.all()):
            actions.append(
                dict(
                    _index=self.index,
                    _type=self.doc_type,
                    _source=obj.to_dict(),
                    _id=obj.id,
                )
            )
        helpers.bulk(self.es, actions)
        return len(actions)


    def delete_by_question_id(self, id):
        return self.execute_delete({"match": {"id": id}})
  
