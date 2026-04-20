"""法规文本切分。"""
from __future__ import annotations

import re
from typing import List


def split_article(full_text: str, max_chars: int = 150, overlap_chars: int = 80) -> List[str]:
    """按语义边界优先切分法规条文。"""
    text = (full_text or "").strip()
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]

    segments: List[str] = []
    start = 0
    delimiters = re.compile(r"[。；;\n]")

    while start < len(text):
        end_limit = min(start + max_chars, len(text))
        if end_limit == len(text):
            piece = text[start:end_limit].strip()
            if piece:
                segments.append(piece)
            break

        candidate = text[start:end_limit]
        matches = list(delimiters.finditer(candidate))
        if matches:
            end = start + matches[-1].end()
        else:
            end = end_limit

        piece = text[start:end].strip()
        if piece:
            segments.append(piece)

        if end >= len(text):
            break

        next_start = max(start + 1, end - overlap_chars)
        if next_start <= start:
            next_start = end
        start = next_start

    return segments
