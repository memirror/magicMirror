# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/6/2

from ..whooshe import wq
from ..es import esq
from ..signal import signal_insert_question, signal_delete_question


@signal_insert_question.connect
def insert_to_whoosh(target):
    wq.write_obj(keyword=target.question, id=target.id)


@signal_insert_question.connect
def insert_to_elasticsearch(target):
    if not esq.ping():
        return
    esq.insert(body={
        k: getattr(target, k)
        for k in target.__table__.columns.keys()
    }, id=target.id)


@signal_delete_question.connect
def delete_from_whoosh(target):
    wq.delete_obj(keyword=target.question)


@signal_delete_question.connect
def delete_from_elasticsearch(target):
    if not esq.ping():
        return
    esq.delete_by_question_id(target.id)
