# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/27

from elasticsearch import Elasticsearch

from .question import ElasticSearchQuestion
from ...setting import ELASTICSEARCH_HOST


ElasticSearchQuestion.es = Elasticsearch(ELASTICSEARCH_HOST)
esq = ElasticSearchQuestion("mm_question")
 
