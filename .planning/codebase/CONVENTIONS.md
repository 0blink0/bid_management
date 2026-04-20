# Coding Conventions

**Analysis Date:** 2026-04-20

## Naming Patterns

**Files:**
- Python模块使用 `snake_case.py`，如 `app/api/v1/knowledge.py`、`app/tools/database/redis.py`。
- Agent实现统一放在 `app/agents/<domain>/agent.py`，如 `app/agents/parser/agent.py`、`app/agents/risk/agent.py`。

**Functions:**
- 函数/方法使用 `snake_case`，如 `create_app()`、`get_settings()`、`query_knowledge()`。
- 内部私有辅助函数以 `_` 前缀命名，如 `ParserAgent._parse_pdf()`、`RiskAgent._detect_risks()`。

**Variables:**
- 普通变量用 `snake_case`，如 `file_content`、`task_id`、`doc_type`。
- 常量采用全大写，如 `GREEN`、`RED`（`run_agent_test.py`）。

**Types:**
- 类名采用 `PascalCase`，如 `BaseAgent`、`KnowledgeItem`、`UploadResponse`。
- Pydantic模型以业务名词命名，不加冗余后缀，如 `AgentRequest`、`FileInfo`。

## Code Style

**Formatting:**
- 格式化工具依赖已声明为 `black`（`requirements-dev.txt`、`pyproject.toml`），但未检测到项目级 `black` 配置文件。
- 代码普遍遵循 4 空格缩进、类型注解优先、三引号 docstring（见 `app/main.py`、`app/config.py`）。

**Linting:**
- 静态检查依赖已声明 `ruff` 与 `mypy`（`requirements-dev.txt`），未检测到 `ruff`/`mypy` 配置文件。
- 约定上保持“导入分组 + 类型注解 + 明确返回值”以兼容未来启用的 lint 规则。

## Import Organization

**Order:**
1. 标准库（如 `os`、`uuid`、`datetime`）
2. 第三方库（如 `fastapi`、`pydantic`、`redis.asyncio`）
3. 项目内模块（`from app...` 或同级相对导入）

**Path Aliases:**
- 未使用路径别名；统一使用包路径 `app.*`（如 `from app.config import get_settings`）。

## Error Handling

**Patterns:**
- API层参数/业务校验失败直接抛 `HTTPException`（`app/api/v1/files.py`）。
- 业务调用层存在“捕获广义异常并返回错误字段”的模式（`app/api/v1/agents.py` 的 `except Exception as e`）。
- 基础设施初始化失败倾向抛 `RuntimeError`（`app/tools/database/redis.py` 的 `get_redis()`）。

## Logging

**Framework:** `print`（当前实现）

**Patterns:**
- 生命周期日志使用 `print()` 输出启动/关闭信息（`app/main.py`）。
- 已声明 `loguru` 依赖但主代码未落地统一 logger；新增代码应优先保持同一层日志策略，不混用多套日志接口。

## Comments

**When to Comment:**
- 中文业务注释用于解释职责边界或流程节点，见 Agent 与 API 模块中的 `# TODO`、步骤注释。
- 对明显业务枚举项使用行内注释补充语义（`app/api/v1/knowledge.py` 中知识库类型列表）。

**JSDoc/TSDoc:**
- 不适用（Python 项目）；采用 Python docstring 作为主文档方式。

## Function Design

**Size:** 
- 路由处理函数保持短小（约 10-30 行），复杂逻辑下沉到 Agent/工具层。

**Parameters:**
- API层优先使用 Pydantic 请求模型（如 `AgentRequest`、`KnowledgeQuery`）。
- Agent处理函数统一接收 `Dict[str, Any]`，通过键值做分流（如 `process()` 内按 `type` 路由）。

**Return Values:**
- API层多返回 Pydantic 响应模型或 `Dict/List`。
- Agent层返回结构化 `Dict[str, Any]`，常含 `status`、`type`、`result/error` 字段。

## Module Design

**Exports:**
- 包模块使用 `__all__` 控制显式导出（`app/tools/llm/__init__.py`、`app/agents/base/memory/__init__.py`）。

**Barrel Files:**
- 存在轻量“聚合导出”文件，仅做导入转发，不承载业务逻辑。

---

*Convention analysis: 2026-04-20*
# Coding Conventions

**Analysis Date:** 2026-04-20

## Naming Patterns

**Files:**
- Python modules use `snake_case.py` (for example `app/api/v1/knowledge.py`, `app/tools/llm/manager.py`).
- Test files use `test_*.py` and map directly to component names (for example `tests/agents/test_parser.py`, `tests/agents/test_risk.py`).

**Functions:**
- Functions and methods use `snake_case` (for example `create_app()` in `app/main.py`, `get_settings()` in `app/config.py`, `test_agent_initialization()` in `tests/agents/test_compliance.py`).
- Async handlers and agent methods are explicitly `async def` when I/O or workflow calls are expected (for example `invoke_agent()` in `app/api/v1/agents.py`, `process()` in `app/agents/parser/agent.py`).

**Variables:**
- Local variables are `snake_case` (for example `file_content`, `file_path`, `doc_type`, `input_data` in `app/api/v1/files.py` and `app/agents/parser/agent.py`).
- Constants are uppercase (for example `GREEN`, `RED`, `YELLOW`, `RESET` in `run_agent_test.py`).

**Types:**
- Class names use `PascalCase` (for example `BaseAgent`, `ParserAgent`, `KnowledgeItem`, `TaskStatusResponse`).
- Typed dict/object payloads are commonly `Dict[str, Any]` for flexible agent I/O (for example `app/agents/base/agent.py`, `app/api/v1/agents.py`).

## Code Style

**Formatting:**
- Tooling is present but centralized config is not detected (`black` and `ruff` declared in `requirements-dev.txt` and `pyproject.toml`; no `[tool.black]` or `[tool.ruff]` sections in `pyproject.toml`).
- Use UTF-8 source and bilingual comments/docstrings where domain terms are Chinese (consistent across `app/main.py`, `app/config.py`, `tests/agents/test_parser.py`).

**Linting:**
- Linting tooling is dependency-driven (`ruff`, `mypy` in `requirements-dev.txt`) with no dedicated lint config file detected in `backend`.
- Type hints are used broadly in app and tests; continue this as the primary static-quality signal (for example `app/tools/llm/base.py`, `app/agents/risk/agent.py`).

## Import Organization

**Order:**
1. Standard library imports (`os`, `sys`, `uuid`, `datetime`, `typing`).
2. Third-party imports (`fastapi`, `pydantic`, `pytest`, `langgraph`).
3. Local app imports (`from app...` or relative imports like `from .agents import ...`).

**Path Aliases:**
- No alias system detected; imports use real package paths from `app` and tests patch `sys.path` in `tests/conftest.py` and `tests/agents/conftest.py`.

## Error Handling

**Patterns:**
- API-layer validation errors use `HTTPException` with explicit status/detail (`app/api/v1/files.py`).
- Service/agent invocation paths may wrap exceptions into response envelopes instead of re-raising (`invoke_agent()` in `app/api/v1/agents.py`).
- Abstract/base contracts use `raise ValueError(...)` for invalid manager state (`set_default()` and `get_llm()` in `app/tools/llm/manager.py`).

## Logging

**Framework:** `print` (no active logging framework wiring detected in runtime paths)

**Patterns:**
- Lifecycle and CLI status output uses `print` directly (`app/main.py`, `run_agent_test.py`).
- `loguru` exists as a dependency in `pyproject.toml` but active usage is not detected in `app/`.

## Comments

**When to Comment:**
- Module-level docstrings are used for intent and responsibility summaries.
- Inline comments mark workflow stages and TODO implementation boundaries (for example in `app/api/v1/knowledge.py`, `app/agents/risk/agent.py`, `app/api/v1/files.py`).

**JSDoc/TSDoc:**
- Not applicable (Python codebase). Python docstrings are standard on modules, classes, and methods.

## Function Design

**Size:** Generally short handlers and thin orchestration methods; business logic currently stub-heavy in agent internals.

**Parameters:** Domain payloads pass as dictionaries for agent orchestration (`process(self, input_data: Dict[str, Any])` pattern in `app/agents/*/agent.py`).

**Return Values:** Prefer dictionary envelopes with status/result fields for agents and Pydantic response models for API boundaries (`UploadResponse`, `AgentResponse`).

## Module Design

**Exports:** Package-level `__init__.py` files are used for package boundaries across `app/`, `app/tools/`, `app/agents/`, `tests/`.

**Barrel Files:** Router/module aggregation uses explicit re-export/aggregation files (for example `app/api/v1/router.py` combines subrouters).

---

*Convention analysis: 2026-04-20*
