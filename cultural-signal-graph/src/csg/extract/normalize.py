from __future__ import annotations

import re


_WHITESPACE_RE = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    lowered = text.strip().lower()
    return _WHITESPACE_RE.sub(" ", lowered)

