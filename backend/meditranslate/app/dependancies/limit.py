from fastapi import Depends
from fastapi_limiter.depends import RateLimiter
import sys
from typing import Any
from meditranslate.app.dependancies.empty import empty_dependency


def rate_limiter_dependency(
    times: int = 1,
    milliseconds: int = 0,
    seconds: int = 0,
    minutes: int = 0,
    hours: int = 0,
    identifier: Any = None,
    callback: Any = None
):
    # Check if pytest is imported
    if "pytest" in sys.modules:
        return Depends(empty_dependency("fastapi limmiter"))

    # Return the RateLimiter dependency
    return Depends(RateLimiter(
        times=times,
        milliseconds=milliseconds,
        seconds=seconds,
        minutes=minutes,
        hours=hours,
        identifier=identifier,
        callback=callback
    ))
