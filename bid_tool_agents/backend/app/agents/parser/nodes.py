"""
Parser Agent Nodes
"""
from typing import Any, Dict


async def format_detection_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """格式检测节点"""
    return {"format_detected": "pdf"}


async def text_extraction_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """文本提取节点"""
    return {"text_extracted": "sample text"}


async def ocr_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """OCR节点"""
    return {"ocr_completed": True}


async def table_extraction_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """表格提取节点"""
    return {"tables_extracted": []}
