# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/27

import click

from magicmirror import Apis
from magicmirror.tools.router import RouterByWeight


router = RouterByWeight
router.apis = Apis


@click.command()
def magicmirror():
    question = input("what do you want to know?[q|quit to exit]")
    while True:
        if question in {"q", "quit"}:
            break
        for detail in router().process("whoosh"):
            api = detail["api"]
            source = detail["source"]
            if api is None:
                raise 
            out = api(question)
            if out:
                logger.info("[from] %s", source)
                print(out)
                break
        else:
            print("sorry, i donot know either")
        question = input("what do you want to know?")


main = magicmirror


if __name__ == '__main__':

    import logging

    logging.basicConfig(format="[%(asctime)s] [%(levelname)s] %(message)s")
    logger = logging.getLogger("magicmirror")
    logger.setLevel(logging.DEBUG)

    magicmirror()
  
