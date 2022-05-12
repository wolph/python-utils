from __future__ import annotations

from . import logger

import loguru

__all__ = ['Logurud']


class Logurud(logger.LoggerBase):
    logger: loguru.Logger

    def __new__(cls, *args, **kwargs):
        # Import at runtime to make loguru an optional dependency
        import loguru
        cls.logger: loguru.Loguru = loguru.logger
        return super().__new__(cls)
