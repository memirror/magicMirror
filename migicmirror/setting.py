# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/27

from collections import ChainMap
from configparser import ConfigParser, ExtendedInterpolation
import os
from pathlib import Path

import yaml

from .root import root

configdir = root.joinpath("magicmirror/config")

class cp:
    p = ConfigParser(interpolation=ExtendedInterpolation(), allow_no_value=True)
    p.read(configdir.joinpath("default.cfg"), encoding="utf-8")
    p.read([
        configdir.joinpath(f"{path.strip()}")
        for path in p["default.paths"]["paths"].split(",")
        if path and os.path.exists(configdir.joinpath(f"{path.strip()}"))
    ])


class yp:
    _path = configdir.joinpath("realtimesearch.yaml")
    with open(_path, encoding="utf-8") as file:
        p = yaml.load(file, Loader=yaml.SafeLoader)


class s:
    p = ChainMap(cp.p, yp.p)


DB_MYSQL_URL = s.p["mysql.sqlalchemy"]["url"]
BAIDU_DEFAULT_HEADERS = s.p["default_headers"]["baidu"]
SOGOU_DEFAULT_HEADERS = s.p["default_headers"]["sogou"]
