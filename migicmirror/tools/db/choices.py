# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/29

import enum

class CheckStatus(enum.Enum):
    inreview = 1  # 审核中
    approve = 2  # 审核通过


class ActionStatus(enum.Enum):
    create = 1
    update = 2
    delete = 3
    review = 4
