# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/29

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship

from . import Model, ModelMixin, ModelDeleteMixin, ModelDateMixin
from .middletable import mm_question_tag


class Tag(Model, ModelMixin, ModelDeleteMixin, ModelDateMixin):

    __tablename__ = "mm_tag"

    id = Column(Integer, primary_key=True)
    tag = Column(String(64), nullable=False, index=True)

    def __init__(self, tag: str):
        self.tag = tag

    def __str__(self):
        return self.tag
