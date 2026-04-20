# Codebase Concerns

**Analysis Date:** 2026-04-20

## Tech Debt

**核心流程仍以占位逻辑为主:**
- Issue: 多个 API 与 Agent 主路径返回空列表、静态成功或 mock 值，未接入服务层/存储层。
- Files: `bid_tool_agents/backend/app/api/v1/knowledge.py`, `bid_tool_agents/backend/app/api/v1/files.py`, `bid_tool_agents/backend/app/api/v1/agents.py`, `bid_tool_agents/backend/app/agents/coordinator/agent.py`, `bid_tool_agents/backend/app/agents/parser/agent.py`, `bid_tool_agents/backend/app/agents/risk/agent.py`, `bid_tool_agents/backend/app/agents/compliance/agent.py`
- Impact: 看似可调用，实际无法完成知识库检索、任务调度、风险识别、合规审查等核心业务闭环。
- Fix approach: 建立 service/repository 层并替换 TODO 分支，接入真实 Agent 注册表与任务状态存储，补充端到端断言（成功+失败+副作用）。

**长期记忆设计与实现不一致:**
- Issue: `LongTermMemory` 仅进程内列表存储，`search_knowledge` 为字符串包含匹配，未对接向量检索。
- Files: `bid_tool_agents/backend/app/agents/base/memory/long_term.py`
- Impact: 重启即丢失，数据规模增大后检索质量和延迟不可控。
- Fix approach: 接入 `Qdrant`/数据库持久化，提供分页与召回阈值策略，内存结构仅做短期缓存。

## Known Bugs

**Qdrant 客户端命名冲突导致初始化风险:**
- Symptoms: 自定义类 `QdrantClient` 与 `qdrant_client.QdrantClient` 同名，在 `__init__` 与 `init_qdrant` 中再次调用 `QdrantClient(...)` 时会递归/歧义。
- Files: `bid_tool_agents/backend/app/tools/database/qdrant.py`
- Trigger: 调用 `init_qdrant()` 或实例化本地 `QdrantClient`。
- Workaround: 将本地类改名（如 `QdrantStore`）并显式别名导入第三方客户端（如 `from qdrant_client import QdrantClient as RawQdrantClient`）。

**测试代码对空 LLM 对象进行 patch:**
- Symptoms: 多个测试使用 `patch.object(agent.llm, "chat", ...)`，但 Agent 默认构造时 `llm_manager=None`，`agent.llm` 为 `None`。
- Files: `bid_tool_agents/backend/tests/agents/test_parser.py`, `bid_tool_agents/backend/tests/agents/test_risk.py`, `bid_tool_agents/backend/tests/agents/test_compliance.py`, `bid_tool_agents/backend/app/agents/parser/agent.py`, `bid_tool_agents/backend/app/agents/risk/agent.py`, `bid_tool_agents/backend/app/agents/compliance/agent.py`
- Trigger: 直接运行相关测试用例。
- Workaround: 在 fixture 中注入可用 LLMManager mock，或改为 patch Agent 内部可替换方法而非 `None` 对象。

## Security Considerations

**默认凭证与跨域策略过宽:**
- Risk: 默认数据库口令为弱口令，且 `cors_origins=["*"]` 同时允许携带凭据。
- Files: `bid_tool_agents/backend/app/config.py`, `bid_tool_agents/backend/app/main.py`
- Current mitigation: 存在 `.env`/YAML 覆盖能力。
- Recommendations: 生产环境禁用默认口令并强制环境注入，按环境白名单配置 CORS，禁止 `*` + credentials 组合。

**上传接口存在内存放大面:**
- Risk: `upload_file` 先 `await file.read()` 全量读入内存，单请求可达 500MB。
- Files: `bid_tool_agents/backend/app/api/v1/files.py`
- Current mitigation: 扩展名白名单与大小阈值已配置。
- Recommendations: 改为分块读取与边写边验，并在网关/ASGI 层设置 request body 限制。

## Performance Bottlenecks

**上传并发下内存扩张快:**
- Problem: 每个上传请求都保留完整文件缓冲，无法线性扩展并发。
- Files: `bid_tool_agents/backend/app/api/v1/files.py`, `bid_tool_agents/backend/app/config.py`
- Cause: 同步式全量读取 + 无流式写入。
- Improvement path: 使用 chunk 流式处理，累计大小超限立即中断。

**长期知识检索是 O(n) 扫描:**
- Problem: `search_knowledge` 按字符串包含遍历列表，缺少索引和向量检索。
- Files: `bid_tool_agents/backend/app/agents/base/memory/long_term.py`
- Cause: 向量化链路未实现。
- Improvement path: 实施 embedding + 向量检索 + top-k/pagination。

## Fragile Areas

**PDF 解析异常被吞没:**
- Files: `bid_tool_agents/backend/app/tools/document/pdf.py`
- Why fragile: `except Exception: pass` 使表格/目录/页提取失败无可观测信号。
- Safe modification: 保留错误上下文并写入返回结构/日志，区分“空结果”与“解析失败”。
- Test coverage: 现有测试未覆盖这些异常路径可观测性。

**Agent 调用成功语义与执行脱钩:**
- Files: `bid_tool_agents/backend/app/api/v1/agents.py`, `bid_tool_agents/backend/app/agents/base/agent.py`
- Why fragile: `/agents/invoke` 直接返回“调用成功”，未绑定真实 graph 执行结果与任务状态。
- Safe modification: 增加 agent registry + 任务持久化，失败路径返回结构化错误码。
- Test coverage: 现有测试多为 `result is not None`，无法兜住行为回归。

## Scaling Limits

**进程内状态阻碍水平扩展:**
- Current capacity: 记忆、任务上下文与部分执行状态以进程内对象为主。
- Limit: 多 worker 状态不一致，滚动重启会丢历史。
- Scaling path: 将状态统一外置到 Redis/PostgreSQL/Qdrant，进程内仅保留短 TTL 缓存。

## Dependencies at Risk

**解析链路依赖重且缺少启动期健康探测:**
- Risk: `PyMuPDF`、`paddleocr`、`python-docx`、`unstructured` 缺失时仅在运行时失败。
- Impact: 故障暴露晚，报错多为泛化异常，定位成本高。
- Migration plan: 应用启动时执行依赖自检并暴露 capability matrix，路由层按能力降级或拒绝。

## Missing Critical Features

**关键业务能力未完成闭环:**
- Problem: 知识库查询/增删、文件列表/删除、Agent 调度、任务状态跟踪均未落地。
- Blocks: 无法支撑可追踪、可复核的正式评审流程。

## Test Coverage Gaps

**测试断言强度不足且缺少 API 集成覆盖:**
- What's not tested: API 路由副作用（文件写入、任务状态更新、知识库变更）、错误码契约、真实依赖集成路径。
- Files: `bid_tool_agents/backend/tests/agents/test_parser.py`, `bid_tool_agents/backend/tests/agents/test_compliance.py`, `bid_tool_agents/backend/tests/agents/test_risk.py`, `bid_tool_agents/backend/tests/conftest.py`
- Risk: 关键回归可在“非空断言”下漏检，且 API 层缺陷无法被测试发现。
- Priority: High

---

*Concerns audit: 2026-04-20*
