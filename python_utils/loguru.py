from __future__ import annotations

from . import logger

import loguru

__all__ = ['Logurud']


class Logurud(logger.LoggerBase):
    logger: loguru.Logger

    def __new__(cls, *args, **kwargs):
        cls.logger: loguru.Loguru = loguru.logger.opt(depth=1)
        return super().__new__(cls)
