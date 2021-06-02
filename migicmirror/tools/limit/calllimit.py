# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/29

import time
import typing
import asyncio
import functools
import contextvars

from functools import wraps
from threading import Thread, Event


class LimitExecuteDuration:

    """
    限制函数执行时间，如函数执行超时则直接结束。
    --- usage:
        def your_func(*args, **kwargs):
            ...
            return ...
        ins = LimitExecuteDuration(seconds=1).run(your_func, *args, **kwargs)
        your_need = ins._result
    """

    def __init__(self, seconds: int = 10):
        self.seconds = seconds
        self._result = None
        self._event = Event()

    def set_event(self):
        self._event.wait(self.seconds)
        self._event.set()

    def execute(self, func, *args, **kwargs):
        if not self._event.is_set():
            result = func(*args, **kwargs)
            self._result = result

    def run(self, func, *args, **kwargs):
        t1 = Thread(target=self.execute, args=(func, *args), kwargs=kwargs)
        t2 = Thread(target=self.set_event, )
        t1.start()
        t2.start()
        t1.join(self.seconds)
        return self


# code from starlette.concurrency
async def run_in_threadpool(
    func: typing.Callable, *args: typing.Any, **kwargs: typing.Any
) -> typing.Any:
    loop = asyncio.get_event_loop()
    if contextvars is not None:
        # Ensure we run in the same context
        child = functools.partial(func, *args, **kwargs)
        context = contextvars.copy_context()
        func = context.run
        args = (child,)
    elif kwargs:
        # loop.run_in_executor doesn't accept 'kwargs', so bind them in here
        func = functools.partial(func, **kwargs)
    return await loop.run_in_executor(None, func, *args)


class LimitExecuteDurationWithAsync:

    def __init__(self, seconds: int = 10):
        self.seconds = seconds
        self._result = None

    async def run(self, func, *args, **kwargs):
        only_marker = kwargs.pop("marker", False)
        if only_marker:
            task = asyncio.create_task(
                func(*args, **kwargs)
            )
        else:
            task = run_in_threadpool(func, *args, **kwargs)
        try:
            ret = await asyncio.wait_for(
                    task, timeout=self.seconds,
                )
            self._result = ret

        except asyncio.TimeoutError:
            if hasattr(task, "cancel"):
                task.cancel()
        except Exception as e:
            print(e)
        finally:
            return self
      
