# Testing Patterns

**Analysis Date:** 2026-04-20

## Test Framework

**Runner:**
- `pytest`（见 `bid_tool_agents/backend/pytest.ini` 与 `bid_tool_agents/backend/tests/pytest.ini`）
- Config: `bid_tool_agents/backend/pytest.ini`

**Assertion Library:**
- 使用 Python 原生 `assert`（所有 `tests/agents/test_*.py`）

**Run Commands:**
```bash
pytest tests/agents/ -v              # Run all agent tests
pytest tests/agents/test_parser.py -v # Run single test file
pytest tests/ -m agent -v            # Run by marker
```

## Test File Organization

**Location:**
- 采用集中式目录：`bid_tool_agents/backend/tests/`，Agent专项测试位于 `bid_tool_agents/backend/tests/agents/`。

**Naming:**
- 文件命名为 `test_*.py`（由 `pytest.ini` 的 `python_files = test_*.py` 强制）。

**Structure:**
```
bid_tool_agents/backend/tests/
├── conftest.py
└── agents/
    ├── conftest.py
    └── test_*.py
```

## Test Structure

**Suite Organization:**
```python
class TestParserAgent:
    @pytest.fixture
    def agent(self):
        from app.agents.parser.agent import ParserAgent
        return ParserAgent()

    @pytest.mark.asyncio
    async def test_parse_pdf(self, agent, sample_text):
        with patch.object(agent.llm, "chat", return_value="解析后的结构化文本"):
            result = await agent.process({"type": "pdf", "content": sample_text})
            assert result is not None
```

**Patterns:**
- Setup pattern: 每个测试类内定义 `agent` fixture 动态导入实例（如 `tests/agents/test_compliance.py`）。
- Teardown pattern: 未见显式 teardown；以轻量对象创建为主。
- Assertion pattern: 先断言初始化属性，再断言结果非空或关键字段值（如 `agent_id`、`name`、memory 状态）。

## Mocking

**Framework:** `unittest.mock`（`patch.object`、`AsyncMock`、`MagicMock`）

**Patterns:**
```python
with patch.object(agent.llm, "chat", return_value="mocked"):
    result = await agent.process({"content": sample_text, "check_type": "full"})
    assert result is not None
```

**What to Mock:**
- 外部依赖调用（LLM `chat`/`embeddings`）在单测中优先 mock（`tests/agents/test_parser.py`、`tests/agents/conftest.py`）。

**What NOT to Mock:**
- Agent基础属性与内存层行为通常不 mock，直接验证真实对象状态（如 `tests/agents/test_compliance.py` 的四层记忆断言）。

## Fixtures and Factories

**Test Data:**
```python
@pytest.fixture
def sample_text():
    return """
    招标项目名称：智慧城市数据中心建设项目
    一、资格要求
    1. 具有独立法人资格的企业
    """
```

**Location:**
- 全局路径修正 fixture：`bid_tool_agents/backend/tests/conftest.py`
- Agent共享 fixture 与文本样本：`bid_tool_agents/backend/tests/agents/conftest.py`

## Coverage

**Requirements:** 未检测到覆盖率阈值强制；仅声明了 `pytest-cov` 依赖（`requirements-dev.txt`）。

**View Coverage:**
```bash
pytest tests/ --cov=app --cov-report=term-missing
```

## Test Types

**Unit Tests:**
- 当前主流测试类型。聚焦单一 Agent 初始化、分支处理与内存行为（`tests/agents/test_*.py`）。

**Integration Tests:**
- 标记体系已预留 `integration`（`pytest.ini`），但当前样例以 mock 驱动，真实外部系统集成测试较少。

**E2E Tests:**
- Not used（未检测到 Playwright/Selenium/接口端到端流水线测试文件）。

## Common Patterns

**Async Testing:**
```python
@pytest.mark.asyncio
async def test_law_retrieval(self, agent):
    result = await agent.process({"content": "资质要求是否合规", "check_type": "law_retrieval"})
    assert result is not None
```

**Error Testing:**
```python
def test_agent_initialization(self, agent):
    assert agent.agent_id == "compliance"
    assert agent.memory is not None
```

---

*Testing analysis: 2026-04-20*
# Testing Patterns

**Analysis Date:** 2026-04-20

## Test Framework

**Runner:**
- `pytest` (declared in `requirements-dev.txt` and `pyproject.toml` optional `dev` deps)
- Config: `bid_tool_agents/backend/pytest.ini` (plus `bid_tool_agents/backend/tests/pytest.ini` mirror)

**Assertion Library:**
- Built-in `pytest` assertions with plain `assert`.

**Run Commands:**
```bash
python run_agent_test.py all            # Run all agent tests via wrapper
pytest tests/agents/ -v                 # Run agent tests directly
pytest tests/ -m agent -v               # Run marker-selected tests
```

## Test File Organization

**Location:**
- Dedicated test tree under `bid_tool_agents/backend/tests/`, with agent-specific coverage in `tests/agents/`.

**Naming:**
- File naming follows `test_*.py` (`pytest.ini` enforces `python_files = test_*.py`).
- Class naming follows `Test*`; function naming follows `test_*` (`pytest.ini` enforces both).

**Structure:**
```
bid_tool_agents/backend/tests/
├── conftest.py
└── agents/
    ├── conftest.py
    └── test_*.py
```

## Test Structure

**Suite Organization:**
```python
class TestParserAgent:
    @pytest.fixture
    def agent(self):
        from app.agents.parser.agent import ParserAgent
        return ParserAgent()

    @pytest.mark.asyncio
    async def test_parse_pdf(self, agent, sample_text):
        with patch.object(agent.llm, "chat", return_value="解析后的结构化文本"):
            result = await agent.process({"type": "pdf", "content": sample_text})
            assert result is not None
```

**Patterns:**
- Setup pattern: fixture-driven object creation at suite level (`agent`, `agent_memory`, `settings`, `llm_manager` in `tests/agents/conftest.py` and `tests/agents/test_*.py`).
- Teardown pattern: explicit teardown fixtures are not detected; tests rely on in-memory/ephemeral objects.
- Assertion pattern: behavioral sanity assertions (`is not None`) plus selected field assertions for memory state.

## Mocking

**Framework:** `unittest.mock` (`patch.object`, occasional `AsyncMock`, `MagicMock` imports)

**Patterns:**
```python
with patch.object(agent.llm, "chat", return_value='{"risks": [{"level": "high"}]}'):
    result = await agent.process({"type": "risk_detection", "content": sample_text})
    assert result is not None
```

**What to Mock:**
- LLM chat calls and external model behavior are mocked in agent tests (`tests/agents/test_compliance.py`, `tests/agents/test_parser.py`, `tests/agents/test_risk.py`).

**What NOT to Mock:**
- Agent memory-layer interactions are exercised directly with real in-process memory classes (`tests/agents/test_parser.py`, `tests/agents/test_compliance.py`).

## Fixtures and Factories

**Test Data:**
```python
@pytest.fixture
def sample_text():
    return """
    招标项目名称：智慧城市数据中心建设项目
    ...  # trimmed
    """
```

**Location:**
- Global path/bootstrapping fixture: `tests/conftest.py`.
- Agent-focused fixtures and sample domain text: `tests/agents/conftest.py`.

## Coverage

**Requirements:** No enforced minimum threshold detected.

**View Coverage:**
```bash
pytest --cov=app --cov-report=term-missing
```

## Test Types

**Unit Tests:**
- Dominant type. Per-agent tests validate initialization, method dispatch, and memory operations in isolation.

**Integration Tests:**
- Marker exists (`integration` in `pytest.ini`) but concrete integration suites are not detected in current tree.

**E2E Tests:**
- Not detected.

## Common Patterns

**Async Testing:**
```python
@pytest.mark.asyncio
async def test_compliance_check(self, agent, sample_text):
    result = await agent.process({"content": sample_text, "check_type": "full"})
    assert result is not None
```

**Error Testing:**
```python
def test_agent_initialization(self, agent):
    assert agent.agent_id == "parser"
    assert agent.name == "文档解析Agent"
```

---

*Testing analysis: 2026-04-20*
