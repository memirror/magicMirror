# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/29

import enum

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, DateTime, Boolean, Text, BIGINT
from sqlalchemy_utils import ChoiceType, UUIDType

from ..choices import ActionStatus, CheckStatus
from . import Model, ModelMixin, ModelDateMixin, ModelDeleteMixin

class Answer(Model, ModelMixin, ModelDateMixin, ModelDeleteMixin):

    __tablename__ = "mm_answer"

    id = Column(Integer, primary_key=True)
    answer = Column(Text, nullable=False)

    status = Column(ChoiceType(CheckStatus, impl=Integer()))
    action = Column(ChoiceType(ActionStatus, impl=Integer()))

    create_by = Column(UUIDType(binary=False), ForeignKey("mm_user.id", ondelete="CASCADE"))
    modify_by = Column(UUIDType(binary=False), ForeignKey("mm_user.id", ondelete="CASCADE"))

    role_id = Column(Integer, ForeignKey("mm_role.id", ondelete="CASCADE"))
    question_id = Column(BIGINT, ForeignKey("mm_question.id", ondelete="CASCADE"))

    def __init__(self, answer: str, status: int = 2, action: int = 1):
        self.answer = answer
        self.status = status
        self.action = action

    def __str__(self):
        return self.answer
