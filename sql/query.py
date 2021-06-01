# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/6/1

from sqlalchemy import text, func

from magicmirror.tools.db import _session
from magicmirror.tools.db import User, Role, Permission
from magicmirror.tools.db import Question, Answer, Tag
from magicmirror.tools.db import Record
from magicmirror.tools.db.models.middletable import mm_question_tag, mm_role_permission, mm_question_question


most_tag = (
    _session.query(mm_question_tag)
    .with_entities(mm_question_tag.c.tag, func.count(mm_question_tag.c.tag).label("num"))
    .group_by(mm_question_tag.c.tag)
    .order_by(func.count(mm_question_tag.c.tag).desc())
    .first()
)

question_with_most_answer = (
    _session.query(Question).join(Answer, Answer.question_id == Question.id)
    .with_entities(Question.question, text("count(1) num"), func.group_concat(Answer.answer, "|"))
    .group_by(Answer.question_id, Question.question)
    .order_by(text("count(1) desc"))
    .first()
)

subquery = (
    _session.query(Question)
    .with_entities(
        Question.question, Question.create_by, Question.create_date,
        func.row_number().over(partition_by=Question.create_by, order_by=Question.create_date.desc()).label("rk"))
    .subquery()
)
user_recent_create_detail = _session.query(subquery).filter(subquery.c.rk == 1).first()
