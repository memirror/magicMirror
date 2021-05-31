# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/29

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship

from . import Model, ModelMixin, ModelDateMixin, ModelDeleteMixin
from .middletable import mm_role_permission


class Role(Model, ModelMixin, ModelDateMixin, ModelDeleteMixin):

    role = Column(String(64), primary_key=True)
    permissions = relationship(
        "Permission", secondary=mm_role_permission, back_populates="roles",
    )

    def __init__(self, role: str):
        self.role = role

    def __str__(self):
        return self.role
