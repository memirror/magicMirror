# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/27

import datetime
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from ...root import root
from ... import setting

verbose = True
logger = logging.getLogger("magicmirror.db.session")

def session_factory(bind):
    return sessionmaker(
        bind=bind,
        autocommit=False,
        autoflush=True,
        expire_on_commit=True,
    )


if hasattr(setting, "DB_URL"):
    engine = create_engine(
        setting.DB_URL,
        poolclass=NullPool, pool_recycle=3600, pool_pre_ping=True
    )
else:
    sqlite_path = root.joinpath("magicmirror/mm.db")
    engine = create_engine(
        "sqlite:///{}".format(sqlite_path),
        echo=0, connect_args={"check_same_thread": False}
    )
    logger.info("use sqlite as sql engine, db path --> %s", str(sqlite_path.absolute()))

session = session_factory(engine)

def run():
    global session
    session.close_all()
    session = session_factory(engine)
    if verbose:
        print(datetime.datetime.now())
        print("...restart session...")
        print("\n")


def keep_session_alive(verbose=verbose):
    if verbose:
        print("--keep session alive---".center(50, "-"))
    scheduler = BackgroundScheduler()
    scheduler.add_job(run, "interval", seconds=60*60*5)
    scheduler.start()


keep_session_alive()
