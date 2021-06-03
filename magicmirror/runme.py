# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/27

import logging

import click

from magicmirror import Apis
from magicmirror.tools.router import RouterByWeight
from magicmirror.tools.db import Record
from magicmirror.tools.limit.calllimit import LimitExecuteDuration
from magicmirror.tools.cache import SimpleCache


logging.basicConfig(format="[%(asctime)s] [%(levelname)s] %(message)s")
logger = logging.getLogger("magicmirror")

router = RouterByWeight
router.apis = Apis
cache = SimpleCache(threshold=300, default_timeout=10)


def makeprefix(q):
    return "mm:question:{}".format(q)


def mm(question):

    nq = makeprefix(question)
    out = mm.cache.get(nq)
    if out:
        logger.info("[cache] [real source] %s", out["source"])
        return {"out": out["out"], "source": "cache " + out["source"]}

    for detail in router().process():
        api = detail["api"]
        source = detail["source"]
        if api is None:
            raise
        out = api(question)
        if out:
            ret = {"out": out, "source": source}
            mm.cache.set(nq, ret)
            return ret


@click.command()
@click.option(
    "--loglevel", "-l",
    default="warn", required=False, type=str,
    help="logging level",
)
def magicmirror(loglevel):
    logger.setLevel(getattr(logging, loglevel.upper()))
    question = input("what do you want to know?[q|quit to exit]")
    while True:
        if question in {"q", "quit"}:
            break
        ret = LimitExecuteDuration(5).run(mm, question)._result
        record = Record(question=question, answer="", source="")
        if ret:
            logger.info("[from] %s", ret["source"])
            record.source = ret["source"]
            record.answer = ret["out"]
            print(ret["out"])
        else:
            print("sorry, i donot know either")
        record.save()
        question = input("what do you want to know?")


mm.cache = cache
main = magicmirror


if __name__ == '__main__':

    magicmirror()
