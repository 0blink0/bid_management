#!/usr/bin/env python3
"""将 BAAI/bge-m3 下载到项目内固定目录，便于国内网络与离线加载。"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

REPO_ID = "BAAI/bge-m3"


def default_model_dir() -> Path:
    from app.domain.knowledge_ingest.vectorizer import default_bge_m3_storage_dir

    return default_bge_m3_storage_dir()


def _cleanup_hf_partial(dest: Path) -> None:
    temp = dest / "._____temp"
    if temp.exists():
        shutil.rmtree(temp, ignore_errors=True)


def _download_hf_mirror(dest: Path) -> None:
    os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
    from huggingface_hub import snapshot_download

    dest.mkdir(parents=True, exist_ok=True)
    snapshot_download(repo_id=REPO_ID, local_dir=str(dest))


def _download_modelscope(dest: Path) -> None:
    try:
        from modelscope.hub.snapshot_download import snapshot_download as ms_snapshot_download
    except ImportError as exc:  # pragma: no cover - runtime helper
        raise RuntimeError('请先安装 modelscope：pip install modelscope -i https://mirrors.aliyun.com/pypi/simple') from exc

    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        shutil.rmtree(dest)
    try:
        ms_snapshot_download(REPO_ID, local_dir=str(dest))
    except TypeError:
        cached_path = Path(ms_snapshot_download(REPO_ID, cache_dir=str(dest.parent)))
        shutil.copytree(cached_path, dest)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="下载 BAAI/bge-m3 到本地目录（先 hf-mirror，失败再 ModelScope）")
    p.add_argument(
        "--dest",
        type=Path,
        default=None,
        help="目标目录（默认 backend/storage/models/BAAI-bge-m3）",
    )
    p.add_argument(
        "--skip-hf-mirror",
        action="store_true",
        help="跳过 hf-mirror，直接使用 ModelScope",
    )
    return p


def main() -> int:
    from app.domain.knowledge_ingest.vectorizer import bge_m3_local_ready

    args = build_parser().parse_args()
    dest = (args.dest or default_model_dir()).resolve()
    print(f"目标目录: {dest}")

    if bge_m3_local_ready(dest):
        print("模型已就绪（含主权重），跳过下载。")
        return 0

    _cleanup_hf_partial(dest)

    if not args.skip_hf_mirror:
        try:
            print("步骤 1/2: 从 hf-mirror 下载 …")
            _download_hf_mirror(dest)
            if bge_m3_local_ready(dest):
                print("下载成功（hf-mirror）。")
                return 0
            print("hf-mirror 未得到完整权重，将尝试 ModelScope。")
        except Exception as exc:  # noqa: BLE001
            print(f"hf-mirror 失败: {exc}")
            print("将尝试 ModelScope。")

    try:
        print("步骤 2/2: 从 ModelScope 下载 …")
        _download_modelscope(dest)
    except Exception as exc:  # noqa: BLE001
        print(f"ModelScope 失败: {exc}")
        return 1

    if not bge_m3_local_ready(dest):
        print("下载结束但未检测到完整模型（缺少 config/modules 或主权重过小）。")
        return 1

    print("下载成功（ModelScope / 回退路径）。")
    return 0


if __name__ == "__main__":
    if __package__ is None or __package__ == "":
        sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    sys.exit(main())
