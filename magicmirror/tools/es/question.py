# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/6/1

import enum

from elasticsearch import helpers

from .base import ElastciSearchCore
from ..db import Question


class ElasticSearchQuestion(ElastciSearchCore):

    def insert(self, body, id):
        origin = body
        new = origin.copy()
        new["action"] = origin["action"].value if isinstance(origin["action"], enum.Enum) else origin["action"]
        new["status"] = origin["status"].value if isinstance(origin["status"], enum.Enum) else origin["status"]
        new["uid"] = origin["uid"].hex
        for date in ("create_date", "update_date", "delete_date"):
            datavalue = origin[date]
            if datavalue:
                new[date] = str(datavalue)
        super().insert(new, id)

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
