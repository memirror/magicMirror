# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/27

from collections import ChainMap
from configparser import ConfigParser, ExtendedInterpolation
import os

import yaml

from magicmirror.root import root

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

    ps = []
    paths = os.listdir(configdir)
    for path in paths:
        if not path.endswith(("yaml", "yml")):
            continue
        path = configdir.joinpath(path)
        with open(path, encoding="utf-8") as file:
            ps.append(yaml.load(file, Loader=yaml.SafeLoader))
    p = ChainMap(*ps)


class s:
    p = ChainMap(cp.p, yp.p)


DB_MYSQL_URL = s.p["mysql.sqlalchemy"]["url"]
BAIDU_DEFAULT_HEADERS = s.p["default_headers"]["baidu"]
SOGOU_DEFAULT_HEADERS = s.p["default_headers"]["sogou"]
DB_URL = DB_MYSQL_URL

ELASTICSEARCH_HOST = s.p["elasticsearch"]["host"]
