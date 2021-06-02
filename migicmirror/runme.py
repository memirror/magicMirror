# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/27

import logging

import click

from magicmirror import Apis
from magicmirror.tools.router import RouterByWeight
from magicmirror.tools.limit.calllimit import LimitExecuteDuration


logging.basicConfig(format="[%(asctime)s] [%(levelname)s] %(message)s")
logger = logging.getLogger("magicmirror")
logger.setLevel(logging.DEBUG)

router = RouterByWeight
router.apis = Apis


def mm(question):
    for detail in router().process():
        api = detail["api"]
        source = detail["source"]
        if api is None:
            raise
        out = api(question)
        if out:
            return {"out": out, "source": source}


@click.command()
def magicmirror():
    question = input("what do you want to know?[q|quit to exit]")
    while True:
        if question in {"q", "quit"}:
            break
        ret = LimitExecuteDuration(1).run(mm, question)._result
        if ret:
            logger.info("[from] %s", ret["source"])
            print(ret["out"])
        else:
            print("sorry, i donot know either")
        question = input("what do you want to know?")


main = magicmirror


if __name__ == '__main__':

    magicmirror()
 
