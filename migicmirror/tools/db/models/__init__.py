# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/27

from datetime import datetime

from sqlalchemy import DateTime, Column, Boolean
from sqlalchemy.orm import relationship, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from ..session import session, engine

_session = scoped_session(session)

Model = declarative_base(name="Model")


class ModelMixin(object):

    query = objects = _session.query_property()

    def delete(self):
        _session.delete(self)
        _session.commit()

    def save(self):
        _session.add(self)
        _session.commit()

    def to_dict(self):
        return {
            obj: getattr(self, obj)
            for obj in self.__class__.__table__.columns.keys()
        }


class ModelDateMixin(object):

    delete_date = Column(DateTime, nullable=True)
    create_date = Column(DateTime, default=datetime.now)
    update_date = Column(DateTime, nullable=True, onupdate=datetime.now)


class ModelDeleteMixin(object):

    is_delete = Column(Boolean, default=False)


from . import answer, middletable, permission, question, record, role, user, tag
