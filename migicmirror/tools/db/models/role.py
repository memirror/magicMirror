# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/29

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, DateTime
from sqlalchemy_utils.types import UUIDType

from . import Model, ModelMixin, ModelDateMixin, ModelDeleteMixin

class Role(Model, ModelMixin, ModelDateMixin, ModelDeleteMixin):

    __tablename__ = "mm_role"

    id = Column(Integer, primary_key=True)
    role = Column(String(32), unique=True, nullable=True, index=True)
    permission_id = Column(Integer, ForeignKey("mm_permission.id"))

    def __init__(self, role: str):
        self.role = role

    def __str__(self):
        return self.role
