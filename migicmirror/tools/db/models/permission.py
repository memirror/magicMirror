# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/29

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, DateTime, Boolean

from . import Model, ModelMixin, ModelDateMixin, ModelDeleteMixin

class Permission(Model, ModelMixin, ModelDateMixin, ModelDeleteMixin):

    __tablename__ = "mm_permission"

    id  = Column(Integer, primary_key=True)
    lookover_question = Column(Boolean, default=False)
    edit_question = Column(Boolean, default=False)
    add_question = Column(Boolean, default=False)
    delete_question = Column(Boolean, default=False)

    lookover_answer = Column(Boolean, default=False)
    edit_answer = Column(Boolean, default=False)
    add_answer = Column(Boolean, default=False)
    delete_answer = Column(Boolean, default=False)

    lookover_tag = Column(Boolean, default=False)
    edit_tag = Column(Boolean, default=False)
    add_tag = Column(Boolean, default=False)
    delete_tag = Column(Boolean, default=False)

    def __init__(self,
                 lookover_question: bool = False, edit_question: bool = False, add_question: bool = False, delete_question: bool = False,
                 lookover_answer: bool = False, edit_answer: bool = False, add_answer: bool = False, delete_answer: bool = False,
                 lookover_tag: bool = False, edit_tag: bool = False, add_tag: bool = False, delete_tag: bool = False):
        self.lookover_question = lookover_question
        self.edit_question = edit_question
        self.add_question = add_question
        self.delete_question = delete_question

        self.lookover_answer = lookover_answer
        self.edit_answer = edit_answer
        self.add_answer = add_answer
        self.delete_answer = delete_answer

        self.lookover_tag = lookover_tag
        self.edit_tag = edit_tag
        self.add_tag = add_tag
        self.delete_tag = delete_tag

