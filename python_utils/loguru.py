from __future__ import annotations
import typing

import loguru

from . import logger as logger_module

__all__ = ['Logurud']


class Logurud(logger_module.LoggerBase):
    logger: loguru.Logger

    def __new__(cls, *args: typing.Any, **kwargs: typing.Any):
        cls.logger: loguru.Logger = loguru.logger.opt(depth=1)
        return super().__new__(cls)
