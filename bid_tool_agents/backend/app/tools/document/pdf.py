"""
PDF专项解析器
"""
from typing import List, Dict, Any, Optional
import fitz  # PyMuPDF


class PDFParser:
    """
    PDF解析器 - 基于PyMuPDF

    功能:
    - 文字提取
    - 表格提取
    - 图片提取
    - 目录提取
    - 元数据读取
    """

    def __init__(self):
        self.supported_formats = ['.pdf']

    async def parse(
        self,
        file_path: str,
        extract_images: bool = True,
        extract_tables: bool = True
    ) -> Dict[str, Any]:
        """
        解析PDF

        Args:
            file_path: PDF文件路径
            extract_images: 是否提取图片
            extract_tables: 是否提取表格

        Returns:
            解析结果
        """
        result = {
            "success": False,
            "file_path": file_path,
            "pages": 0,
            "text": "",
            "elements": [],
            "metadata": {},
            "error": None
        }

        try:
            doc = fitz.open(file_path)
            result["pages"] = len(doc)
            result["metadata"] = doc.metadata

            all_text = []

            for page_num in range(len(doc)):
                page = doc[page_num]

                # 提取文字
                text = page.get_text("text")
                all_text.append(text)
                result["elements"].append({
                    "type": "text",
                    "page": page_num + 1,
                    "content": text
                })

                # 提取表格
                if extract_tables:
                    tables = self._extract_tables_from_page(page, page_num)
                    result["elements"].extend(tables)

                # 提取图片
                if extract_images:
                    images = self._extract_images_from_page(page, page_num)
                    result["elements"].extend(images)

            result["text"] = "\n\n".join(all_text)
            result["success"] = True

        except Exception as e:
            result["error"] = str(e)

        return result

    def _extract_tables_from_page(self, page, page_num: int) -> List[Dict[str, Any]]:
        """从页面提取表格"""
        tables = []

        # 尝试使用PyMuPDF的表格检测
        try:
            table_dict = page.find_tables()
            for table_idx, table in enumerate(table_dict.tables):
                table_data = []
                for row in table.rows:
                    row_data = [cell.text for cell in row.cells]
                    table_data.append(row_data)

                tables.append({
                    "type": "table",
                    "page": page_num + 1,
                    "table_index": table_idx,
                    "bbox": table.bbox,
                    "content": table_data
                })
        except Exception:
            # 表格检测失败，忽略
            pass

        return tables

    def _extract_images_from_page(self, page, page_num: int) -> List[Dict[str, Any]]:
        """从页面提取图片"""
        images = []

        for img_idx, img in enumerate(page.get_images()):
            xref = img[0]
            base_image = page.parent.extract_image(xref)

            images.append({
                "type": "image",
                "page": page_num + 1,
                "image_index": img_idx,
                "xref": xref,
                "width": base_image["width"],
                "height": base_image["height"],
                "colorspace": base_image["colorspace"],
                "bpc": base_image["bpc"],
                "ext": base_image["ext"]
            })

        return images

    async def extract_toc(self, file_path: str) -> List[Dict[str, Any]]:
        """提取目录"""
        toc = []

        try:
            doc = fitz.open(file_path)
            toc = doc.get_toc()
        except Exception:
            pass

        return toc

    async def get_page_text(self, file_path: str, page_num: int) -> str:
        """获取指定页文字"""
        try:
            doc = fitz.open(file_path)
            if 0 <= page_num < len(doc):
                return doc[page_num].get_text("text")
        except Exception:
            pass
        return ""
