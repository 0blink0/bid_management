# Phase 1: 法规数据入库底座 - Pattern Map

**Mapped:** 2026-04-20  
**Files analyzed:** 10  
**Analogs found:** 10 / 10

## File Classification

| 建议新增/修改文件 | 角色 | 数据流位置 | 推荐复用来源 | 匹配度 |
|---|---|---|---|---|
| `bid_tool_agents/backend/app/domain/knowledge_ingest/models.py` | model | transform | `bid_tool_agents/backend/app/api/v1/knowledge.py`（Pydantic 建模） | role-match |
| `bid_tool_agents/backend/app/domain/knowledge_ingest/loader.py` | service | file-I/O -> transform | `bid_tool_agents/backend/app/api/v1/files.py`（文件与输入校验） | role+flow-match |
| `bid_tool_agents/backend/app/domain/knowledge_ingest/chunker.py` | service | transform | `bid_tool_agents/backend/app/tools/document/parser.py`（按类型分派 + 结构化结果） | flow-match |
| `bid_tool_agents/backend/app/domain/knowledge_ingest/vectorizer.py` | service | request-response -> transform | `bid_tool_agents/backend/app/tools/llm/api/qwen.py`（LLM 调用接口层） | flow-match |
| `bid_tool_agents/backend/app/domain/knowledge_ingest/writer.py` | service | CRUD | `bid_tool_agents/backend/app/tools/database/qdrant.py`（collection/create/upsert/delete） | exact |
| `bid_tool_agents/backend/app/domain/knowledge_ingest/audit.py` | service | event-driven / append-log | `bid_tool_agents/backend/app/tools/database/postgres.py`（记录模型与全局初始化模式） | role-match |
| `bid_tool_agents/backend/app/scripts/ingest_laws.py` | script | batch | `bid_tool_agents/backend/run_agent_test.py`（argparse + main 入口） | exact |
| `bid_tool_agents/backend/tests/knowledge_ingest/test_loader.py` | test | file-I/O | `bid_tool_agents/backend/tests/agents/test_parser.py` + `tests/conftest.py` | exact |
| `bid_tool_agents/backend/tests/knowledge_ingest/test_writer.py` | test | CRUD | `bid_tool_agents/backend/tests/agents/test_parser.py` + `tests/agents/conftest.py` | role-match |
| `bid_tool_agents/backend/tests/knowledge_ingest/test_idempotent_rebuild.py` | test | batch / CRUD | `bid_tool_agents/backend/tests/agents/test_parser.py` | flow-match |

## Pattern Assignments

### `app/domain/knowledge_ingest/models.py`（model, transform）

**Analog:** `bid_tool_agents/backend/app/api/v1/knowledge.py`  
**用途:** 使用 Pydantic 定义标准输入输出实体，承载 `article_no/chunk_id/version/source_file`。

**建模模式**（`knowledge.py` 12-27）：
```python
class KnowledgeItem(BaseModel):
    id: str
    type: str
    title: str
    content: str
    metadata: Dict[str, Any]

class KnowledgeQuery(BaseModel):
    query: str
    knowledge_type: Optional[str] = None
    limit: int = 10
```

---

### `app/domain/knowledge_ingest/loader.py`（service, file-I/O -> transform）

**Analog:** `bid_tool_agents/backend/app/api/v1/files.py`  
**用途:** 先做严格预检（JSON 解析/必填字段）再进入下游；不通过即 fail-fast。

**输入校验+fail-fast 模式**（`files.py` 39-47）：
```python
file_content = await file.read()
if len(file_content) > settings.storage.max_file_size:
    raise HTTPException(status_code=400, detail="File too large")

ext = os.path.splitext(file.filename)[1].lower()
if ext not in settings.storage.allowed_extensions:
    raise HTTPException(status_code=400, detail="File type not allowed")
```

**配置注入模式**（`files.py` 11-16）：
```python
from app.config import get_settings
settings = get_settings()
```

---

### `app/domain/knowledge_ingest/chunker.py`（service, transform）

**Analog:** `bid_tool_agents/backend/app/tools/document/parser.py`  
**用途:** 条目分段流程可复用“按条件分派 + 统一结果对象”的组织方式。

**分派模式**（`parser.py` 100-117）：
```python
ext = file_path.split('.')[-1].lower()
if ext == 'pdf':
    return await self._parse_pdf(file_path)
elif ext in ['doc', 'docx']:
    return await self._parse_docx(file_path)
else:
    return ParseResult(success=False, content="", elements=[], metadata={}, error=f"Unsupported file type: {ext}")
```

**结构化结果对象模式**（`parser.py` 47-55）：
```python
@dataclass
class ParseResult:
    success: bool
    content: str
    elements: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    error: Optional[str] = None
```

---

### `app/domain/knowledge_ingest/vectorizer.py`（service, request-response -> transform）

**Analog:** `bid_tool_agents/backend/app/tools/llm/api/qwen.py`  
**用途:** 统一向量化接口（文本列表入参 -> 向量列表出参），并对 provider 未实现场景显式抛错。

**接口骨架模式**（`qwen.py` 67-70）：
```python
async def embeddings(self, texts: List[str]) -> List[List[float]]:
    # TODO: 实现阿里云embedding API
    raise NotImplementedError("Embedding not implemented for AliQwen")
```

**HTTP 调用与配置注入模式**（`qwen.py` 21-35）：
```python
async with httpx.AsyncClient(timeout=self.config.timeout) as client:
    response = await client.post(
        self.API_URL,
        headers={"Authorization": f"Bearer {self.api_key}"},
        json={"model": self.config.model.value, "messages": messages}
    )
```

---

### `app/domain/knowledge_ingest/writer.py`（service, CRUD）

**Analog:** `bid_tool_agents/backend/app/tools/database/qdrant.py`  
**用途:** 复用集合生命周期与 upsert 路径，落实 `force=true` 重建门禁与 `laws_regulations` 写入。

**集合创建模式**（`qdrant.py` 15-33）：
```python
def create_collection(self, collection_name: str, vector_size: int = 1536, distance: Distance = Distance.COSINE) -> bool:
    collections = self.client.get_collections().collections
    if collection_name in [c.name for c in collections]:
        return True
    self.client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_size, distance=distance)
    )
    return True
```

**批量 upsert 模式**（`qdrant.py` 35-42）：
```python
def upsert(self, collection_name: str, points: List[PointStruct]) -> bool:
    self.client.upsert(collection_name=collection_name, points=points)
    return True
```

**全局初始化模式**（`qdrant.py` 76-91）：
```python
_qdrant: Optional[QdrantClient] = None

def init_qdrant(url: str, port: int = 6333) -> QdrantClient:
    global _qdrant
    _qdrant = QdrantClient(url=url, port=port)
    return _qdrant
```

---

### `app/domain/knowledge_ingest/audit.py`（service, event-driven / append-log）

**Analog:** `bid_tool_agents/backend/app/tools/database/postgres.py`  
**用途:** 审计记录可复用“记录实体 + created_at/updated_at + 初始化获取器”模式。

**记录模型模式**（`postgres.py` 55-68）：
```python
class TaskRecord(Base):
    __tablename__ = "task_records"
    task_id = Column(String(64), unique=True, nullable=False, index=True)
    status = Column(String(32), nullable=False)
    input_data = Column(Text)
    result = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
```

**初始化/获取模式**（`postgres.py` 37-49）：
```python
def init_database(url: str) -> Database:
    global _db
    _db = Database(url)
    _db.create_tables()
    return _db

def get_database() -> Database:
    if _db is None:
        raise RuntimeError("Database not initialized")
    return _db
```

---

### `app/scripts/ingest_laws.py`（script, batch）

**Analog:** `bid_tool_agents/backend/run_agent_test.py`  
**用途:** 复用 CLI 入口风格，提供 `--force`、`--version`、`--input` 参数与退出码。

**argparse + main 模式**（`run_agent_test.py` 85-97, 140-141）：
```python
def main():
    parser = argparse.ArgumentParser(description="运行Agent测试")
    parser.add_argument("agent", nargs="?", default="all")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

if __name__ == "__main__":
    main()
```

**退出码模式**（`run_agent_test.py` 133-137）：
```python
sys.exit(0 if passed == total else 1)
sys.exit(0 if success else 1)
```

---

### `tests/knowledge_ingest/test_loader.py`（test, file-I/O）

**Analog:** `bid_tool_agents/backend/tests/agents/test_parser.py` + `tests/conftest.py`  
**用途:** 单测结构沿用 `Test*` 类、fixture 注入与异常路径断言。

**测试类与异步用例模式**（`test_parser.py` 8-25）：
```python
class TestParserAgent:
    @pytest.fixture
    def agent(self):
        from app.agents.parser.agent import ParserAgent
        return ParserAgent()

    @pytest.mark.asyncio
    async def test_parse_pdf(self, agent, sample_text):
        ...
```

**测试路径初始化模式**（`tests/conftest.py` 4-10）：
```python
import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

---

### `tests/knowledge_ingest/test_writer.py`（test, CRUD）

**Analog:** `bid_tool_agents/backend/tests/agents/test_parser.py` + `tests/agents/conftest.py`  
**用途:** 使用 fixture 管理 mock 依赖，覆盖正常写入/写入失败/集合不存在等分支。

**Mock 模式**（`test_parser.py` 27-36）：
```python
with patch.object(agent.llm, 'chat', return_value="解析后的结构化文本"):
    result = await agent.process({"type": "pdf", "content": sample_text})
    assert result is not None
```

**共享 fixture 模式**（`tests/agents/conftest.py` 43-54）：
```python
@pytest.fixture
def mock_llm_response():
    async def mock_chat(messages, **kwargs):
        return "这是Mock LLM的响应"
    async def mock_embeddings(texts):
        return [[0.1, 0.2, 0.3] for _ in texts]
    return mock_chat, mock_embeddings
```

---

### `tests/knowledge_ingest/test_idempotent_rebuild.py`（test, batch / CRUD）

**Analog:** `bid_tool_agents/backend/tests/agents/test_parser.py`  
**用途:** 用两次执行对比断言幂等结果，覆盖 `force=False` 拒绝与 `force=True` 成功重建。

**状态断言模式**（`test_parser.py` 77-84）：
```python
immediate = agent.memory.immediate.get(f"parser:{task_id}")
assert immediate is not None
context = agent.memory.short_term.get_task_context(task_id)
assert context is not None
```

## Shared Patterns

### 配置读取（全链路通用）
**Source:** `bid_tool_agents/backend/app/config.py`  
**Apply to:** `loader.py`, `writer.py`, `vectorizer.py`, `ingest_laws.py`
```python
class VectorDBConfig(BaseSettings):
    host: str = "localhost"
    port: int = 6333
    collection_name: str = "bid_documents"
    vector_size: int = 1536

@lru_cache()
def get_settings() -> Settings:
    env = os.getenv("ENV", "development")
    return load_config_from_yaml(env)
```

### API/服务层错误表达
**Source:** `bid_tool_agents/backend/app/api/v1/files.py`, `bid_tool_agents/backend/app/api/v1/agents.py`  
**Apply to:** loader/vectorizer/writer（统一结构化错误明细）
```python
raise HTTPException(status_code=400, detail="File type not allowed")

except Exception as e:
    return AgentResponse(success=False, agent_id=request.agent_id, error=str(e))
```

### 路由聚合与模块边界
**Source:** `bid_tool_agents/backend/app/api/v1/router.py`  
**Apply to:** Phase 2 API 化时复用（Phase 1 保持脚本入口）
```python
router.include_router(agents_router, prefix="/agents", tags=["Agent"])
router.include_router(files_router, prefix="/files", tags=["Files"])
router.include_router(knowledge_router, prefix="/knowledge", tags=["Knowledge"])
```

### 数据库客户端“初始化 + 获取”单例模式
**Source:** `bid_tool_agents/backend/app/tools/database/qdrant.py`, `postgres.py`  
**Apply to:** `writer.py`, `audit.py`
```python
def get_qdrant() -> QdrantClient:
    if _qdrant is None:
        raise RuntimeError("Qdrant not initialized")
    return _qdrant
```

## No Analog Found

无“完全无类比”文件；但以下为**部分匹配**（需在实现时补设计）：

| 文件 | 原因 |
|---|---|
| `app/domain/knowledge_ingest/vectorizer.py` | 现有 `embeddings` 在 `qwen.py` 为 TODO，只有接口骨架，无可直接复用实现 |
| `app/domain/knowledge_ingest/chunker.py` | 仓库无“法规条文语义分段+overlap”现成实现，仅有文档解析分派模式可借鉴 |

## Metadata

**Analog search scope:**  
- `bid_tool_agents/backend/app/api/v1`  
- `bid_tool_agents/backend/app/tools/database`  
- `bid_tool_agents/backend/app/tools/document`  
- `bid_tool_agents/backend/app/tools/llm/api`  
- `bid_tool_agents/backend/tests`  
- `bid_tool_agents/backend`

**Files scanned:** 12  
**Pattern extraction date:** 2026-04-20
