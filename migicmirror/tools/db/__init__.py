# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/27


import logging

from sqlalchemy_utils import create_database, database_exists, drop_database

from .models import Model
from .models.user import User
from .models.role import Role
from .models.permission import Permission
from .models.question import Question
from .models.answer import Answer
from .models.tag import Tag
from .models.record import Record
from .models import _session, engine

logger = logging.getLogger("magicmirror.db")

class BuildDatabase(object):

    _force_dabase_rebuild: bool = False
    _force_tables_rebuild: bool = False

    def create_database(self) -> None:
        is_create_db = True
        if database_exists(engine.url):
            if self._force_dabase_rebuild:
                logger.warning("database <%s> exists and will be droped to rebuild", engine.url.database)
                drop_database(engine.url)
            else:
                is_create_db = False
        if is_create_db:
            create_database(engine.url, encoding="utf8mb4")
            logger.warning("database <%s> create success", engine.url.database)

    def create_tables(self):
        check_first = self._force_tables_rebuild
        Model.metadata.create_all(bind=engine, checkfirst=check_first)

    def create_permission(self) -> None:
        Permission("add question").save()
        Permission("query question").save()
        Permission("edit question").save()
        Permission("delete question").save()

        Permission("add answer").save()
        Permission("edit answer").save()
        Permission("delete answer").save()

        Permission("add tag").save()
        Permission("edit tag").save()
        Permission("delete tag").save()

    def create_role(self) -> Role:
        r = Role(role="admin")
        r.permissions = Permission.query.all()
        r.save()
        return r

    def create_user(self) -> User:
        u = User(name="admin", password="secret", phone="", email="admin@admin.com", is_activate=True)
        u.save()
        return u

    def run(self):
        self.create_database()
        self.create_tables()
        self.create_permission()
        role_admin = self.create_role()
        u = self.create_user()
        u.role = role_admin
        u.save()

