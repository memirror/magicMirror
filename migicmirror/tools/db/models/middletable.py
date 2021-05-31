# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/29

from sqlalchemy import Table
from sqlalchemy import Column, ForeignKey
from sqlalchemy import BIGINT, DateTime, Integer, String
from sqlalchemy import func

from . import Model


# 问题 <-> 相似问题
mm_question_question = Table(
    "mm_question_question", Model.metadata,
    Column("similarity_with", BIGINT, ForeignKey("mm_question.id"), primary_key=True),
    Column("similarity_to", BIGINT, ForeignKey("mm_question.id"), primary_key=True),
    Column("create_date", DateTime, default=func.now()),
)

# 问题 <-> 所属类目
mm_question_tag = Table(
    "mm_question_tag", Model.metadata,
    Column("question_id", BIGINT, ForeignKey("mm_question.id"), primary_key=True),
    Column("tag", String(64), ForeignKey("mm_tag.tag"), primary_key=True),
    Column("create_date", DateTime, default=func.now()),
)

# 角色 <-> 权限
mm_role_permission = Table(
    "mm_role_permission", Model.metadata,
    Column("role", String(64), ForeignKey("mm_role.role"), primary_key=True),
    Column("permission", String(128), ForeignKey("mm_permission.permission"), primary_key=True),
    Column("create_date", DateTime, default=func.now())

)

