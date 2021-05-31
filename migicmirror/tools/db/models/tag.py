# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/29

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship

from . import Model, ModelMixin, ModelDeleteMixin, ModelDateMixin


class Tag(Model, ModelMixin, ModelDeleteMixin, ModelDateMixin):

    tag = Column(String(64), primary_key=True)
    questions = relationship(
        "Question", secondary="mm_question_tag", back_populates="tags",
    )

    def __init__(self, tag: str):
        self.tag = tag

    def __str__(self):
        return self.tag
