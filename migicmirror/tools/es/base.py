# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/6/1

from dataclasses import dataclass

from elasticsearch import Elasticsearch
from elasticsearch import helpers


@dataclass
class ElasticSearchBase(object):
    index: str = None
    es: Elasticsearch = None
    doc_type: str = "magicmirror"


class ElasticSearchMixin(object):

    def ping(self):
        return self.es.ping()

    def info(self):
        return self.es.info()

    def count(self, body):
        """
        .count(
            {"query":
                {
                    "range": {"create_date": {"lt": "2020-10-10"}}
                }
            }
        )
        :param body:
        :return:
        """
        return self.es.count(
            index=self.index,
            doc_type=self.doc_type,
            body=body,
        )["count"]

    @property
    def get_max_id(self):
        """获取当前es中最大id
        用来增量更新
        """
        dsl = {
            "aggs": {
                "maxid": {
                    "max": {
                        "field": "id"}
                }
            }
        }
        r = self.es.search(
            index=self.index,
            body=dsl,
            doc_type=self.doc_type,
            filter_path=["aggregations"],
        )
        return r.get("aggregations", {}).get("maxid", {}).get("value")


class ElasticSearchSearch(ElasticSearchBase):
    def search(self, keyword, size=5, indicate="question", show_highlight=False):
        dsl = {
            "query": {
                "match": {
                    indicate: keyword,
                }
            },
            "highlight": {
                "require_field_match": True,
                # "pre_tags": "<b style="color:red;font-size:24px">",
                # "post_tags": "</b>",
                "fields": {
                    indicate: {},
                    # "*": {},
                }
            },
        }
        rets = self.es.search(
            index=self.index, body=dsl, size=size,
            doc_type=self.doc_type,
            filter_path=["hits.hits._source", "hits.hits.highlight"],
        )

        hits = [obj for obj in rets.get("hits", {}).get("hits", [])]
        if show_highlight:
            for hit in hits:
                hit["_source"]["_highlight:{}".format(indicate)] = hit.pop("highlight", {}).get(indicate, [])
        hits = [obj["_source"] for obj in hits]
        return hits


class ElasticSearchUpdate(ElasticSearchSearch):

    def insert(self, body, id):

        self.es.index(
            index=self.index,
            doc_type=self.doc_type,
            body=body,
            id=id,
        )

    def update_by_query(self, body=None):
        """用于批量更新字段"""
        """
        body = {
            "script": {
                "lang": "painless",
                "inline": "if (ctx._source.status == null){ctx._source.status=3}"
                #"inline": "ctx._source.kw_sourceType= 'trueTime'"   #新增字段kw_sourceType值为trueTime
            }
        }
        """
        self.es.update_by_query(
            index=self.index,
            doc_type=self.doc_type,
            body=body,
        )

    def update(self, indicate, oldvalue, newvalue):
        _update_num = 0
        num, e = self._update(indicate, oldvalue, newvalue)
        while num:
            _update_num += num
            num, e = self._update(indicate, oldvalue, newvalue)
        return _update_num

    def _update(self, indicate, oldvalue, newvalue):
        actions = []
        for detail in self.search(keyword=oldvalue, indicate=indicate, size=300):
            if not detail[indicate] == oldvalue:
                continue
            id = detail["id"]
            action = {
                "_op_type": "update",
                "_index": self.index,
                "_type": "_doc",
                "_id": id,
                "script": {
                    "inline": f"ctx._source.{indicate}={newvalue}",
                }
            }
            actions.append(action)
        return helpers.bulk(client=self.es, actions=actions, index=self.index)


class ElastciSearchDelete(ElasticSearchBase):

    def execute_delete(self, query):
        self.es.delete_by_query(
            index=self.index,
            body={"query": query},
            doc_type=self.doc_type,
        )
        return True

    def delete_index(self):
        self.es.indices.delete(self.index)

    def clear(self):
        return self.execute_delete({"match_all": {}})


class ElastciSearchCore(ElasticSearchMixin, ElasticSearchUpdate, ElastciSearchDelete):

    def __init__(self, index: str):
        self.index = index
  
