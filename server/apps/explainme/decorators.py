from __future__ import annotations
import functools
import re
from typing import Callable, TYPE_CHECKING


if TYPE_CHECKING:
    from server.apps.explainme.scraper import ExplainmeScraper


class ToUserFriendlyInterface:
    @staticmethod
    def description(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(self: ExplainmeScraper) -> str:
            # making clear description without html hrefs
            full_explanation = await func(self)
            pattern = r'href\s*=\s*["\'][^"\']*["\']'
            __cleaned_full_explanation = re.sub(pattern, '', str(full_explanation[0])[1:-1])
            return __cleaned_full_explanation

        return wrapper
