# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/31

import os
import logging
import shutil
from typing import Any, NoReturn, Generator

from whoosh.fields import Schema, TEXT, NUMERIC
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
from jieba.analyse import ChineseAnalyzer

from ...root import root


logger = logging.getLogger("magicmirror.whoosh")


class WhooshBase(object):

    index_name: str = ""
    analyser = ChineseAnalyzer()
    whoosh_dir = root.joinpath("whooshe")

    def _mkdir(self, force_rebuild: bool) -> NoReturn:
        self.index_dir = self.whoosh_dir.joinpath(f"{self.index_name}")
        if os.path.exists(self.index_dir):
            if force_rebuild:
                shutil.rmtree(self.index_dir)
                logger.warning("[delete][dir] %s", self.index_dir)
            else:
                return
        os.makedirs(self.index_dir)
        logger.warning("[makedirs] %s", self.index_dir)
        self._mkindex()

    def _mkindex(self) -> NoReturn:
        schema = Schema(
            keyword=TEXT(stored=True, analyzer=self.analyser),
            id=NUMERIC(stored=True, unique=True)
        )
        create_in(self.index_dir, schema, self.index_name)

    def preprocess(self, force_rebuild: bool) -> NoReturn:
        self._mkdir(force_rebuild)

    def __init__(self, force_rebuild: bool = False):

        self.preprocess(force_rebuild)

        self.ix = open_dir(self.index_dir, self.index_name)
        self.parse = QueryParser("keyword", schema=self.ix.schema).parse

    def search(self, keyword: str, topk: int = 5) -> Generator:
        q = self.parse(keyword)
        with self.ix.searcher() as searcher:
            hits = searcher.search(q, limit=topk)
        return hits

    def delete_obj(self, keyword: str) -> bool:
        q = self.parse(keyword)
        with self.ix.searcher() as searcher:
            hits = searcher.search(q, limit=10)
            for hit in hits:
                if hit.get("keyword") == keyword:
                    with self.ix.writer() as writer:
                        writer.delete_document(docnum=hit.docnum)
                    return True
        return False

    def write_obj(self, keyword: str, id: Any) -> NoReturn:
        with self.ix.writer() as writer:
            writer.add_document(keyword=keyword, id=id)

    def update_obj(self, keyword: str, id: Any) -> NoReturn:
        with self.ix.writer() as writer:
            writer.update_document(keyword=keyword, id=id)
