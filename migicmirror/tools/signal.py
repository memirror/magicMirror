# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/6/2

from blinker import signal


signal_delete_question = signal("delete-question")
signal_insert_question = signal("insert-question")
  
