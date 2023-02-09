from __future__ import annotations

import loguru

from . import logger as logger_module, types

__all__ = ['Logurud']


class Logurud(logger_module.LoggerBase):
    logger: loguru.Logger

    def __new__(cls, *args: types.Any, **kwargs: types.Any) -> Logurud:
        cls.logger: loguru.Logger = loguru.logger.opt(depth=1)
        return super().__new__(cls)
