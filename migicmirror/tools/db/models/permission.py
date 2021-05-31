# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/29

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship

from . import Model, ModelMixin, ModelDateMixin, ModelDeleteMixin
from .middletable import mm_role_permission


class Permission(Model, ModelMixin, ModelDateMixin, ModelDeleteMixin):

    permission = Column(String(128), primary_key=True)
    roles = relationship(
        "Role", secondary=mm_role_permission, back_populates="permissions",
    )

    def __init__(self, permission: str):
        self.permission = permission

    def __str__(self):
        return self.permission
