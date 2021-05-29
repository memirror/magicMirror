# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/29

import enum
import uuid

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import String, Integer, DateTime, Boolean, BIGINT
from sqlalchemy_utils.types import UUIDType, ChoiceType

from ..choices import ActionStatus, CheckStatus
from . import Model, ModelMixin, ModelDateMixin, ModelDeleteMixin
from .middletable import mm_question_question, mm_question_tag


class Question(Model, ModelMixin, ModelDateMixin, ModelDeleteMixin):

    __tablename__ = "mm_question"

    id = Column(BIGINT, primary_key=True)
    uid = Column(UUIDType(binary=False), unique=True, index=True, default=uuid.uuid4)
    question = Column(String(512), nullable=False, index=True, unique=True)

    status = Column(ChoiceType(CheckStatus, impl=Integer()))

    create_by = Column(UUIDType(binary=False), ForeignKey("mm_user.id", ondelete="CASCADE"))
    modify_by = Column(UUIDType(binary=False), ForeignKey("mm_user.id", ondelete="CASCADE"))

    action = Column(ChoiceType(ActionStatus, impl=Integer()))
    role_id = Column(Integer, ForeignKey("mm_role.id", ondelete="CASCADE"))

    tags = relationship("Tag", secondary=mm_question_tag, backref="questions")
    answers = relationship("Answer", cascade="all, delete-orphan")
    similarity_with = relationship("Question", secondary=mm_question_question,
                                primaryjoin=(mm_question_question.c.similarity_to == id),
                                secondaryjoin=(mm_question_question.c.similarity_with == id),
                                backref="similarity_to")

    def __init__(self, question: str, status: int = 2, action: int = 1):
        self.question = question
        self.status = status
        self.action = action

    def __str__(self):
        return self.question
