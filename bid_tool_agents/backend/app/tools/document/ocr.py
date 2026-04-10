"""
OCR处理器

支持多种OCR引擎:
1. PaddleOCR (推荐) - 开源中文支持好
2. EasyOCR - 轻量级
3. Tesseract - 经典开源OCR
"""
from typing import List, Dict, Any, Optional, Tuple
from abc import ABC, abstractmethod
import numpy as np
from PIL import Image


class BaseOCRProcessor(ABC):
    """OCR处理器基类"""

    @abstractmethod
    async def recognize(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """识别文字"""
        pass

    @abstractmethod
    async def recognize_file(self, file_path: str) -> Dict[str, Any]:
        """识别文件"""
        pass


class PaddleOCRProcessor(BaseOCRProcessor):
    """
    PaddleOCR处理器

    优点:
    - 开源免费
    - 中文支持好
    - 支持多种语言
    - 可本地部署

    安装:
        pip install paddlepaddle paddleocr
    """

    def __init__(self, use_gpu: bool = False, lang: str = 'ch'):
        """
        Args:
            use_gpu: 是否使用GPU
            lang: 语言选项 'ch', 'en', 'ch_det_en_rec'
        """
        self.use_gpu = use_gpu
        self.lang = lang
        self._engine = None

    def _get_engine(self):
        """获取或初始化引擎"""
        if self._engine is None:
            from paddleocr import PaddleOCR
            self._engine = PaddleOCR(
                use_angle_cls=True,
                lang=self.lang,
                use_gpu=self.use_gpu,
                show_log=False
            )
        return self._engine

    async def recognize(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """识别文字"""
        engine = self._get_engine()
        result = engine.ocr(image, cls=True)

        items = []
        if result and result[0]:
            for line in result[0]:
                bbox = line[0]
                text = line[1][0]
                confidence = line[1][1]

                items.append({
                    "text": text,
                    "confidence": confidence,
                    "bbox": bbox
                })

        return items

    async def recognize_file(self, file_path: str) -> Dict[str, Any]:
        """识别文件"""
        engine = self._get_engine()
        result = engine.ocr(file_path, cls=True)

        items = []
        full_text = []
        total_confidence = 0

        if result and result[0]:
            for line in result[0]:
                bbox = line[0]
                text = line[1][0]
                confidence = line[1][1]

                items.append({
                    "text": text,
                    "confidence": confidence,
                    "bbox": bbox
                })
                full_text.append(text)
                total_confidence += confidence

        avg_confidence = total_confidence / len(items) if items else 0

        return {
            "success": True,
            "items": items,
            "full_text": "\n".join(full_text),
            "lines": len(items),
            "avg_confidence": avg_confidence
        }


class EasyOCRProcessor(BaseOCRProcessor):
    """
    EasyOCR处理器

    优点:
    - 开源免费
    - 支持多种语言
    - 使用简单

    安装:
        pip install easyocr
    """

    def __init__(self, languages: List[str] = ['ch_sim', 'en']):
        self.languages = languages
        self._engine = None

    def _get_engine(self):
        """获取或初始化引擎"""
        if self._engine is None:
            import easyocr
            self._engine = easyocr.Reader(self.languages, gpu=False)
        return self._engine

    async def recognize(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """识别文字"""
        engine = self._get_engine()
        result = engine.readtext(image)

        items = []
        for bbox, text, confidence in result:
            items.append({
                "text": text,
                "confidence": confidence,
                "bbox": bbox
            })

        return items

    async def recognize_file(self, file_path: str) -> Dict[str, Any]:
        """识别文件"""
        engine = self._get_engine()
        result = engine.readfile(file_path)

        items = []
        full_text = []

        for bbox, text, confidence in result:
            items.append({
                "text": text,
                "confidence": confidence,
                "bbox": bbox
            })
            full_text.append(text)

        return {
            "success": True,
            "items": items,
            "full_text": "\n".join(full_text),
            "lines": len(items)
        }


class OCRProcessorFactory:
    """OCR处理器工厂"""

    @staticmethod
    def create(backend: str = "paddleocr", **kwargs) -> BaseOCRProcessor:
        """
        创建OCR处理器

        Args:
            backend: 'paddleocr', 'easyocr', 'tesseract'
        """
        if backend == "paddleocr":
            return PaddleOCRProcessor(
                use_gpu=kwargs.get("use_gpu", False),
                lang=kwargs.get("lang", "ch")
            )
        elif backend == "easyocr":
            return EasyOCRProcessor(
                languages=kwargs.get("languages", ["ch_sim", "en"])
            )
        else:
            raise ValueError(f"Unknown OCR backend: {backend}")
