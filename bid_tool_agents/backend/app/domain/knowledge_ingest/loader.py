"""JSONL 法规加载与预检。"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import List, Sequence

from .chunker import split_article
from .models import LawRecord, validate_required_fields

ARTICLE_RE = re.compile(r"(第[一二三四五六七八九十百千万0-9]+条)")
REPO_ROOT = Path(__file__).resolve().parents[5]


def build_stable_chunk_id(title: str, chapter: str, content: str) -> str:
    """生成稳定 chunk 标识。"""
    raw = f"{title}|{chapter}|{content}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def extract_article_no(content: str, preferred: str | None = None) -> str:
    """提取条号。"""
    if preferred and preferred.strip():
        return preferred.strip()
    match = ARTICLE_RE.search(content or "")
    if match:
        return match.group(1)
    return "未知条号"


def _resolve_source_file(path: Path, repo_root: Path | None = None) -> str:
    base = repo_root or REPO_ROOT
    resolved = path.resolve()
    try:
        return resolved.relative_to(base.resolve()).as_posix()
    except ValueError:
        # 测试临时目录或跨盘符场景下，回退为绝对路径避免抛错。
        return resolved.as_posix()


def load_jsonl_records(input_paths: Sequence[str], version: str) -> List[LawRecord]:
    """读取并预检 JSONL，输出结构化记录。"""
    if not version or not version.strip():
        raise ValueError("version is required")
    records: List[LawRecord] = []

    for input_path in input_paths:
        file_path = Path(input_path)
        source_file = _resolve_source_file(file_path)

        with file_path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, start=1):
                line_text = line.strip()
                if not line_text:
                    continue
                try:
                    item = json.loads(line_text)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"{source_file}:{line_no} invalid json: {exc.msg}") from exc

                item["version"] = version
                item["source_file"] = source_file
                validate_required_fields(item, source_file, line_no)

                title = str(item["title"]).strip()
                chapter = str(item["chapter"]).strip()
                content = str(item["content"]).strip()
                article_no = extract_article_no(content, item.get("article_no"))
                base_chunk_id = build_stable_chunk_id(title, chapter, content)
                chunks = split_article(content)

                if not chunks:
                    raise ValueError(f"{source_file}:{line_no} empty content after splitting")

                for idx, chunk in enumerate(chunks):
                    chunk_id = base_chunk_id if len(chunks) == 1 else f"{base_chunk_id}-{idx}"
                    records.append(
                        LawRecord(
                            title=title,
                            chapter=chapter,
                            article_no=article_no,
                            content=content,
                            source_file=source_file,
                            chunk_id=chunk_id,
                            version=version,
                            full_text=content,
                            chunk_text=chunk,
                        )
                    )

    return records
