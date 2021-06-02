# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/6/2

import json
import logging

from magicmirror.tools.db import *
from magicmirror.tools.db import _session as session
from magicmirror.tools.whooshe import wq
from magicmirror.tools.es import esq

logging.basicConfig(format="[%(asctime)s] [%(levelname)s] %(message)s")
logger = logging.getLogger("magicmirror")
logger.setLevel(logging.INFO)


def _add_or_commit():
    counter: int = 0

    def __add_or_commit(instance, batch=100):
        nonlocal counter

        session.add(instance)
        if counter >= batch:
            session.commit()
            counter = 0

    return __add_or_commit


add_or_commit = _add_or_commit()


if __name__ == '__main__':

    rebuild_db = True
    rebuild_elasticsesarch = True
    rebuild_whoosh = True

    if rebuild_db:
        BuildDatabase._force_database_rebuild = True
        BuildDatabase().run()

    if rebuild_elasticsesarch:
        esq.clear()

    if rebuild_whoosh:
        wq.clear()

    with open("dataset/mm_dataset.json", encoding="utf-8") as file:
        mm_dataset = json.load(file)

    dtags = {tag.tag: tag for tag in Tag.query.all()}
    questions = set([question.question for question in Question.query.all()])
    for line in mm_dataset:
        tags = line["tags"]
        answers = line["answers"]
        question = line["question"]
        
        if question in questions:
            continue

        q = Question(question=question)
        q.answers = [Answer(answer=answer) for answer in answers]
        for tag in tags:
            if tag not in dtags:
                dtags[tag] = Tag(tag=tag).create()
            q.tags.append(dtags[tag])
        add_or_commit(q)
    session.commit()
