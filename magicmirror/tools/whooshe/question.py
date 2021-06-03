# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/31

from .base import WhooshBase


class QuestionWhoosh(WhooshBase):
    index_name: str = "question"

    def write_objs(self, objs):
        with self.ix.writer() as writer:
            for obj in objs:
                writer.add_document(keyword=obj.question, id=obj.id)

    def search(self, keyword: str, topk: int = 5) -> list:
        q = self.parse(keyword)
        with self.ix.searcher() as searcher:
            hits = searcher.search(q, limit=topk)
            hits = [
                {"question": hit["keyword"], "id": hit["id"]}
                for hit in hits
            ]
        return hits
