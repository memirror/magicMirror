# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/29

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, DateTime, Boolean, Text

from . import Model, ModelMixin, ModelDeleteMixin, ModelDateMixin
from .middletable import mm_question_tag


class Record(Model, ModelMixin, ModelDateMixin):

    __tablename__ = "mm_record"

    id = Column(Integer, primary_key=True)
    question = Column(String(512), index=True)
    answer = Column(Text)
    source = Column(String(64))

    def __init__(self, question: str, answer: str, source: str):
        self.question = question
        self.answer = answer
        self.source = source

    def __str__(self):
        return f"""
        <from> {self.source}
        <question> {self.question}
        <answer> {self.answer}
        """
