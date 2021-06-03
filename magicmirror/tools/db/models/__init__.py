# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/27

import re
from datetime import datetime

from sqlalchemy.orm import scoped_session
from sqlalchemy import DateTime, Column, Boolean
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative import declarative_base

from ..session import session, engine


_session = scoped_session(session)
Model = declarative_base(name="Model")


def camel2snake(name: str) -> str:
    name = re.sub("[A-Z]", lambda obj: "_" + obj.group()[0].lower(), name)
    if not name.startswith("_"):
        name = "_" + name
    return name


class ModelMixin(object):

    query = objects = _session.query_property()

    @declared_attr
    def __tablename__(cls):
        return "mm" + camel2snake(cls.__name__)

    def delete(self):
        _session.delete(self)
        _session.commit()

    def save(self):
        _session.add(self)
        _session.commit()

    def create(self):
        self.save()
        return self

    def to_dict(self):
        return {
            obj: getattr(self, obj)
            for obj in type(self).__table__.columns.keys()
        }


class ModelDateMixin(object):

    create_date = Column(DateTime, default=datetime.now)
    update_date = Column(DateTime, nullable=True, onupdate=datetime.now)


class ModelDeleteMixin(object):

    is_delete = Column(Boolean, default=False)
    delete_date = Column(DateTime, nullable=True)


from . import answer, middletable, permission, question, record, role, user, tag
  
