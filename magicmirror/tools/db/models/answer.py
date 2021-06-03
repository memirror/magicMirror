# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/29

import uuid

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, Text, BIGINT, String
from sqlalchemy_utils import ChoiceType, UUIDType

from .question import Question
from ..choices import ActionStatus, CheckStatus
from . import Model, ModelMixin, ModelDateMixin, ModelDeleteMixin, _session


class Answer(Model, ModelMixin, ModelDateMixin, ModelDeleteMixin):

    id = Column(Integer, primary_key=True)
    uid = Column(UUIDType(binary=False), unique=True, index=True, default=uuid.uuid4)
    answer = Column(Text, nullable=False)

    status = Column(ChoiceType(CheckStatus, impl=Integer()))
    action = Column(ChoiceType(ActionStatus, impl=Integer()))

    create_by = Column(String(64), ForeignKey("mm_user.name", ondelete="CASCADE"))
    modify_by = Column(String(64), ForeignKey("mm_user.name", ondelete="CASCADE"))

    question_id = Column(BIGINT, ForeignKey("mm_question.id", ondelete="CASCADE"))

    def __init__(self, answer: str, status: int = 2, action: int = 1):
        self.answer = answer
        self.status = status
        self.action = action

    def __str__(self):
        return self.answer

    @property
    def question(self):
        return _session.query(Question).get(self.question_id).question
