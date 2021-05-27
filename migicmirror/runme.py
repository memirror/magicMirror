# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/27

import click

from magicmirror.realtimespider import realtimespider


@click.command()
def magicmirror():
    question = input("what do you want to know?")
    while True:
        out = realtimespider(question)
        if out:
            print(out)
        else:
            print("sorry, i donot know either")
        question = input("what do you want to know?")


main = magicmirror


if __name__ == '__main__':

    magicmirror()
