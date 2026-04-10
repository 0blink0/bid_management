"""
文档解析器 - 支持多种方案

文档解析方案选择:

1. 【推荐】本地PaddleOCR + PyMuPDF
   - 完全开源，无需API
   - 适合私有化部署
   - 支持中文识别良好

2. 【备选】marker-pdf (本地PDF转Markdown)
   - 开源，支持本地运行
   - 基于深度学习，识别效果好
   - 资源消耗较大

3. 【云服务】Unstructured.io (有使用限制)
   - 云服务有15,000页/月免费限制
   - 需要注册账号和API Key
   - 适合快速原型验证

4. 【企业】百度/阿里OCR API
   - 商业服务，按量付费
   - 识别率高，稳定
   - 需要企业认证
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class ParserType(Enum):
    """解析器类型"""
    PDF = "pdf"
    DOCX = "docx"
    IMAGE = "image"
    TABLE = "table"


class ParserBackend(Enum):
    """解析后端"""
    LOCAL = "local"           # 本地（推荐）
    CLOUD = "cloud"           # 云服务
    ENTERPRISE = "enterprise"  # 企业API


@dataclass
class ParseResult:
    """解析结果"""
    success: bool
    content: str
    elements: List[Dict[str, Any]]  # 结构化元素
    metadata: Dict[str, Any]
    error: Optional[str] = None


class BaseDocumentParser(ABC):
    """文档解析基类"""

    @abstractmethod
    async def parse(self, file_path: str) -> ParseResult:
        """解析文档"""
        pass

    @abstractmethod
    async def extract_tables(self, file_path: str) -> List[List[List[str]]]:
        """提取表格"""
        pass

    @abstractmethod
    async def extract_images(self, file_path: str) -> List[Dict[str, Any]]:
        """提取图片"""
        pass


class LocalDocumentParser(BaseDocumentParser):
    """
    本地文档解析器

    使用开源组件:
    - PyMuPDF: PDF文字提取
    - python-docx: Word解析
    - PaddleOCR: 文字识别
    - OpenCV: 图像处理
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self._init_parsers()

    def _init_parsers(self):
        """初始化解析器"""
        # PDF解析器
        self._pdf_parser = None
        # OCR处理器
        self._ocr_processor = None
        # Word解析器
        self._docx_parser = None

    async def parse(self, file_path: str) -> ParseResult:
        """解析文档"""
        ext = file_path.split('.')[-1].lower()

        if ext == 'pdf':
            return await self._parse_pdf(file_path)
        elif ext in ['doc', 'docx']:
            return await self._parse_docx(file_path)
        elif ext in ['jpg', 'jpeg', 'png', 'bmp']:
            return await self._parse_image(file_path)
        else:
            return ParseResult(
                success=False,
                content="",
                elements=[],
                metadata={},
                error=f"Unsupported file type: {ext}"
            )

    async def _parse_pdf(self, file_path: str) -> ParseResult:
        """解析PDF - 使用PyMuPDF"""
        try:
            import fitz  # PyMuPDF

            doc = fitz.open(file_path)
            content_parts = []
            elements = []

            for page_num, page in enumerate(doc):
                # 提取文字
                text = page.get_text()
                content_parts.append(text)
                elements.append({
                    "type": "text",
                    "page": page_num + 1,
                    "content": text
                })

                # 提取表格（简单方法）
                tables = page.extract_tables()
                for idx, table in enumerate(tables):
                    elements.append({
                        "type": "table",
                        "page": page_num + 1,
                        "table_index": idx,
                        "content": table
                    })

                # 提取图片
                images = page.get_images()
                for img_idx, img in enumerate(images):
                    elements.append({
                        "type": "image",
                        "page": page_num + 1,
                        "image_index": img_idx,
                        "xref": img[0]
                    })

            return ParseResult(
                success=True,
                content="\n\n".join(content_parts),
                elements=elements,
                metadata={
                    "pages": len(doc),
                    "title": doc.metadata.get("title", ""),
                    "author": doc.metadata.get("author", "")
                }
            )
        except Exception as e:
            return ParseResult(
                success=False,
                content="",
                elements=[],
                metadata={},
                error=str(e)
            )

    async def _parse_docx(self, file_path: str) -> ParseResult:
        """解析Word - 使用python-docx"""
        try:
            from docx import Document

            doc = Document(file_path)
            content_parts = []
            elements = []

            for para in doc.paragraphs:
                if para.text.strip():
                    content_parts.append(para.text)
                    elements.append({
                        "type": "text",
                        "style": para.style.name,
                        "content": para.text
                    })

            # 提取表格
            for idx, table in enumerate(doc.tables):
                table_data = []
                for row in table.rows:
                    row_data = [cell.text for cell in row.cells]
                    table_data.append(row_data)
                elements.append({
                    "type": "table",
                    "table_index": idx,
                    "content": table_data
                })

            return ParseResult(
                success=True,
                content="\n\n".join(content_parts),
                elements=elements,
                metadata={
                    "paragraphs": len(doc.paragraphs),
                    "tables": len(doc.tables)
                }
            )
        except Exception as e:
            return ParseResult(
                success=False,
                content="",
                elements=[],
                metadata={},
                error=str(e)
            )

    async def _parse_image(self, file_path: str) -> ParseResult:
        """解析图片 - 使用PaddleOCR"""
        try:
            from paddleocr import PaddleOCR

            if self._ocr_processor is None:
                self._ocr_processor = PaddleOCR(
                    use_angle_cls=True,
                    lang='ch',
                    use_gpu=False  # 设置为True使用GPU
                )

            result = self._ocr_processor.ocr(file_path, cls=True)

            content_parts = []
            elements = []

            if result and result[0]:
                for line in result[0]:
                    text = line[1][0]
                    confidence = line[1][1]
                    bbox = line[0]

                    content_parts.append(text)
                    elements.append({
                        "type": "text",
                        "content": text,
                        "confidence": confidence,
                        "bbox": bbox
                    })

            return ParseResult(
                success=True,
                content="\n".join(content_parts),
                elements=elements,
                metadata={
                    "ocr_engine": "paddleocr",
                    "lines": len(elements)
                }
            )
        except Exception as e:
            return ParseResult(
                success=False,
                content="",
                elements=[],
                metadata={},
                error=str(e)
            )

    async def extract_tables(self, file_path: str) -> List[List[List[str]]]:
        """提取表格"""
        result = await self.parse(file_path)
        tables = [e["content"] for e in result.elements if e["type"] == "table"]
        return tables

    async def extract_images(self, file_path: str) -> List[Dict[str, Any]]:
        """提取图片"""
        result = await self.parse(file_path)
        images = [e for e in result.elements if e["type"] == "image"]
        return images


class CloudDocumentParser(BaseDocumentParser):
    """
    云端文档解析器

    使用Unstructured.io云服务（有15,000页/月限制）
    适合快速原型验证，生产环境建议使用LocalDocumentParser
    """

    def __init__(self, api_key: str, config: Optional[Dict[str, Any]] = None):
        self.api_key = api_key
        self.config = config or {}

    async def parse(self, file_path: str) -> ParseResult:
        """使用Unstructured.io云服务"""
        try:
            from unstructured.partition.pdf import partition_pdf

            elements = await partition_pdf(
                filename=file_path,
                api_key=self.api_key,
                strategy="auto"
            )

            content_parts = []
            parsed_elements = []

            for elem in elements:
                text = str(elem)
                content_parts.append(text)
                parsed_elements.append({
                    "type": elem.type,
                    "content": text,
                    "metadata": elem.metadata.__dict__ if hasattr(elem, 'metadata') else {}
                })

            return ParseResult(
                success=True,
                content="\n\n".join(content_parts),
                elements=parsed_elements,
                metadata={"parser": "unstructured.io", "api_key_provided": bool(self.api_key)}
            )
        except Exception as e:
            return ParseResult(
                success=False,
                content="",
                elements=[],
                metadata={},
                error=str(e)
            )

    async def extract_tables(self, file_path: str) -> List[List[List[str]]]:
        """提取表格"""
        result = await self.parse(file_path)
        tables = [
            e["content"].split("\n")
            for e in result.elements
            if "table" in e["type"].lower()
        ]
        return tables

    async def extract_images(self, file_path: str) -> List[Dict[str, Any]]:
        """提取图片"""
        result = await self.parse(file_path)
        return [
            e for e in result.elements
            if "image" in e["type"].lower()
        ]


class DocumentParserFactory:
    """文档解析器工厂"""

    @staticmethod
    def create(backend: ParserBackend = ParserBackend.LOCAL, **kwargs) -> BaseDocumentParser:
        """创建解析器"""
        if backend == ParserBackend.LOCAL:
            return LocalDocumentParser(kwargs.get("config"))
        elif backend == ParserBackend.CLOUD:
            return CloudDocumentParser(
                api_key=kwargs.get("api_key", ""),
                config=kwargs.get("config")
            )
        else:
            raise ValueError(f"Unknown backend: {backend}")
