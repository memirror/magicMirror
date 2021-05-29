# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/29

import uuid
import hashlib

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, DateTime, Boolean
from sqlalchemy_utils.types import UUIDType
from werkzeug.security import generate_password_hash, check_password_hash

from . import Model, ModelMixin, ModelDateMixin, ModelDeleteMixin


class User(Model, ModelMixin, ModelDateMixin, ModelDeleteMixin):

    __tablename__ = "mm_user"

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    name = Column(String(128), nullable=False, index=True)
    phone = Column(String(32), unique=True, index=True)
    email = Column(String(64), unique=True, index=True)
    password_hash = Column(String(128))

    is_activate = Column(Boolean, default=False)

    login_num = Column(Integer, default=0)
    login_fail_num = Column(Integer, default=0)
    last_login_attempt = Column(DateTime)
    last_login_date = Column(DateTime)

    role_id = Column(Integer, ForeignKey("mm_role.id", ondelete="CASCADE"))

    def __init__(self, name: str, phone: str, email: str, is_activate: bool = False,
                 login_num: int = 0, login_fail_num: int = 0):
        self.name = name
        self.phone = phone
        self.email = email
        self.is_activate = is_activate
        self.login_num = login_num
        self.login_fail_num = login_fail_num

    def __str__(self):
        return self.name

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
