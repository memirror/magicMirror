# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/27

import os

import click

@click.command()
@click.option("--packages", "-p", required=True, type=str, multiple=True, help="pip install shortcut")
def install(packages):
    pypi = "https://mirror.baidu.com/pypi/simple"
    virenv = "conda activate magicMirror"
    os.system(f"""
{virenv} && pip install {" ".join(packages)} -i {pypi}
    """)


if __name__ == '__main__':
    install()
  
