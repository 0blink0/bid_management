# Phase 1: 法规数据入库底座 - Research

**Researched:** 2026-04-20  
**Domain:** 法规 JSONL -> 向量库（Qdrant）可重建入库  
**Confidence:** MEDIUM

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
### 入库数据模型
- **D-01:** 在基础字段之外新增 `article_no`（条号）以增强法条级追溯能力。
- **D-02:** `chunk_id` 采用稳定哈希（基于 `title + chapter + content`），保证跨次重建稳定可复现。
- **D-03:** `version` 采用“数据集批次版本”语义（例如 `2026-04-20`），用于重建批次治理。
- **D-04:** `source_file` 存储仓库相对路径，而非绝对路径。

### 切分与向量策略
- **D-05:** 基础切分粒度按“条”处理，与当前 JSONL 结构保持一致。
- **D-06:** 对超长法条采用语义分段 + overlap，而非硬切。
- **D-07:** 向量维度当前固定为 `1536`，与现有 Qdrant 封装默认值一致。
- **D-08:** payload 同时保留“原文全文 + 子片段文本”，兼顾检索与溯源展示。

### 幂等重建策略
- **D-09:** 重建采用“删集合后全量重建”作为主策略，确保结果干净且可预测。
- **D-10:** 重建操作必须显式 `force=true` 才允许执行。
- **D-11:** Phase 1 固定全量重建 `laws_regulations`，不做 chapter/source 级局部重建。
- **D-12:** 记录结构化重建审计信息（时间、输入文件、条目数、版本）。

### 导入执行与容错
- **D-13:** Phase 1 先提供脚本入口，API 触发放在后续 Phase 2 落地。
- **D-14:** 导入失败策略为 fail-fast：单条解析失败即终止本次导入。
- **D-15:** 入库前执行严格预检（JSON 解析 + 必填字段校验），不通过不入库。
- **D-16:** 导入结果输出“摘要 + 错误明细”。

### Claude's Discretion
- 语义分段时的具体 overlap 数值和分段阈值（在不违背 D-06 前提下由实现阶段确定）。
- 审计记录的落地介质（本地文件、数据库表或任务日志）与字段扩展。

### Deferred Ideas (OUT OF SCOPE)
- API 触发导入任务（属于 Phase 2：法规知识库 API）。
- 局部重建（按 `source_file/chapter`）能力，后续可作为增强项评估。
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| INGEST-01 | 系统可从不标记版 JSONL 读取法规数据并完成结构化解析 | 明确 JSONL 行级 schema、预检流程、fail-fast 策略、输入扫描与错误明细格式 |
| INGEST-02 | 系统可将法条内容向量化并写入 `laws_regulations` 集合 | 明确集合创建/删除重建、PointStruct 结构、批量 upsert、向量维度 1536 对齐 |
| INGEST-03 | 系统可为每条法规保存完整元数据（title/chapter/source_file/chunk_id/version） | 明确 payload 字段与 `article_no` 扩展、相对路径规则、稳定 chunk_id 规则 |
| INGEST-04 | 系统支持幂等重建（重复执行入库不会产生不可控重复数据） | 明确 `force=true` + delete/create + stable id + 审计记录输出 |
</phase_requirements>

## Summary

Phase 1 的核心不是“把文件写进 Qdrant”这么简单，而是构建一条可重复执行、可追溯、可诊断的数据生产线。[VERIFIED: `.planning/phases/01-fa-gui-shu-ju-ru-ku-di-zuo/01-CONTEXT.md`] 当前仓库已经有可复用的 Qdrant 接口骨架、配置中心与知识库类型定义，但没有完成法规入库流水线本体（解析、切分、向量化、重建审计）。[VERIFIED: `bid_tool_agents/backend/app/tools/database/qdrant.py`][VERIFIED: `bid_tool_agents/backend/app/config.py`][VERIFIED: `bid_tool_agents/backend/app/api/v1/knowledge.py`]

建议在 Phase 1 只交付“脚本化全量重建通道”，不提前做 API 编排；这与 D-13 一致，也最小化依赖面。[VERIFIED: `01-CONTEXT.md`] 同时必须先修正现有 `qdrant.py` 的命名冲突风险，否则初始化就可能递归/歧义失败，导致后续所有规划建立在不稳定底座上。[VERIFIED: `.planning/codebase/CONCERNS.md`][VERIFIED: `bid_tool_agents/backend/app/tools/database/qdrant.py`]

**Primary recommendation:** 采用“预检 -> 规范化 -> 向量化 -> 分批 upsert -> 审计落盘”的单向流水线，并以 `force` 控制 delete/create 全量重建，确保 `INGEST-01~04` 一次性闭环。

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| 读取不标记版 JSONL 并解析 | API / Backend | Database / Storage | 属于服务端数据处理与校验职责，不应放在前端 [VERIFIED: `docs/dataset/zhaobiao-toubiao/README.md`] |
| 条级切分与超长条语义分段 | API / Backend | — | 切分策略影响检索质量，必须在统一后端管控 [VERIFIED: `01-CONTEXT.md`] |
| 向量写入 `laws_regulations` | Database / Storage | API / Backend | 主体是向量库持久化，后端负责调用与批处理 [VERIFIED: `qdrant.py`] |
| 幂等重建（删除+重建） | Database / Storage | API / Backend | delete/create/upsert 为存储操作，后端负责 `force` 防护 [CITED: https://api.qdrant.tech/api-reference/collections/delete-collection] |
| 审计记录（时间/输入/条数/版本） | API / Backend | Database / Storage | 审计属于任务编排与可观测性输出 [VERIFIED: `01-CONTEXT.md`] |

## Project Constraints (from .cursor/rules/)

- 未检出 `.cursor/rules/**/*.md` 文件，暂无额外 Cursor 级项目规则。 [VERIFIED: glob `.cursor/rules/**/*.md` = 0]
- 仍需遵守仓库内既有约束：数据源必须为不标记版 JSONL、命名对齐 `laws_regulations`、结果可追溯。 [VERIFIED: `AGENTS.md`][VERIFIED: `.planning/PROJECT.md`]

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| FastAPI | `>=0.109.0` | 入库脚本后续 API 化承载 | 当前后端主框架，Phase 2 直接复用 [VERIFIED: `backend/pyproject.toml`] |
| qdrant-client | `>=1.7.0` | 向量集合管理与 points upsert | 已在项目依赖中声明，且现有封装已调用 [VERIFIED: `backend/pyproject.toml`][VERIFIED: `qdrant.py`] |
| pydantic / pydantic-settings | `>=2.5.0 / >=2.1.0` | 配置与结构化校验 | 与当前配置体系一致 [VERIFIED: `backend/pyproject.toml`][VERIFIED: `config.py`] |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| sqlalchemy | `>=2.0.0` | 审计记录持久化（可选） | 若审计从文件升级为数据库表 [VERIFIED: `backend/pyproject.toml`][VERIFIED: `postgres.py`] |
| pytest / pytest-asyncio | `>=7.4.0 / >=0.21.0` | 入库逻辑与异常路径测试 | Phase 1 交付前最小自动化回归 [VERIFIED: `backend/pyproject.toml`][VERIFIED: `tests/pytest.ini`] |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| 全量重建（delete+create） | 基于 stable id 的增量 upsert | 增量成本低，但难保证“脏数据彻底清空”；与 D-09 冲突 [VERIFIED: `01-CONTEXT.md`] |
| 脚本入口 | 直接做 API 触发 | API 体验更好，但超出 Phase 1 范围（D-13） [VERIFIED: `01-CONTEXT.md`] |

**Version verification note:** 当前环境未检测到 Python/pip 可执行命令，无法在本机二次验证安装版本；以上版本来自仓库声明，不等于实际运行时版本。 [VERIFIED: shell `python --version`/`pip --version` not found]

## Architecture Patterns

### System Architecture Diagram

```text
docs/dataset/zhaobiao-toubiao/*.jsonl
        |
        v
[Precheck Loader]
- 文件枚举
- JSON 逐行解析
- 必填字段校验(title/chapter/content)
        |
        v
[Normalizer]
- 提取 article_no
- 计算 stable chunk_id(hash)
- 补全 source_file/version
        |
        v
[Chunker]
- 条级直通
- 超长条语义分段+overlap
        |
        v
[Embedding Builder]
- 生成 1536 向量
        |
        v
[Qdrant Writer]
- force=true -> delete collection -> create collection
- batch upsert PointStruct(id, vector, payload)
        |
        +--------------------+
        v                    |
[Audit Recorder] <-----------+
- start/end time
- input files
- total/success/fail count
- version
```

### Recommended Project Structure
```text
bid_tool_agents/backend/app/
├── domain/knowledge_ingest/          # Phase 1 新增：入库域逻辑
│   ├── models.py                     # 数据模型（LawRecord / IngestResult）
│   ├── loader.py                     # JSONL 读取 + 预检
│   ├── chunker.py                    # 条级/超长条切分
│   ├── vectorizer.py                 # 向量生成接口封装
│   ├── writer.py                     # Qdrant 写入与重建
│   └── audit.py                      # 审计记录落地
├── scripts/
│   └── ingest_laws.py                # Phase 1 脚本入口（force 开关）
└── tools/database/qdrant.py          # 复用并修复命名冲突
```

### Pattern 1: Precheck-First Ingestion
**What:** 任何向量写入之前，先做输入文件与行级字段预检，失败即终止。  
**When to use:** 需要 fail-fast 与可追溯入库。  
**Example:**
```python
# Source: project pattern + D-14/D-15
for line_no, raw in enumerate(file, start=1):
    item = json.loads(raw)  # parse check
    for field in ("title", "chapter", "content"):
        if not item.get(field):
            raise ValueError(f"missing {field} at {path}:{line_no}")
```

### Pattern 2: Force-Gated Rebuild
**What:** 只有显式 `force=true` 才允许 delete/create 全量重建。  
**When to use:** 避免误删生产集合，保障幂等重建可控。  
**Example:**
```python
if not force:
    raise ValueError("Rebuild requires force=true")
client.delete_collection(collection_name=collection)
client.create_collection(collection_name=collection, vectors_config=VectorParams(size=1536, distance=Distance.COSINE))
```
Source: [CITED: https://api.qdrant.tech/api-reference/collections/delete-collection] [CITED: https://api.qdrant.tech/api-reference/collections/create-collection]

### Anti-Patterns to Avoid
- **只做 upsert 不清库：** 会保留历史脏数据，破坏 D-09 的“干净重建”目标。 [VERIFIED: `01-CONTEXT.md`]
- **使用绝对路径作为 source_file：** 破坏跨环境可重现性。 [VERIFIED: D-04 in `01-CONTEXT.md`]
- **随机 chunk_id：** 无法保证重复执行稳定映射，幂等性退化。 [VERIFIED: D-02]
- **静默吞异常：** 现有代码已有 `except Exception: pass` 风险，Phase 1 不能延续。 [VERIFIED: `.planning/codebase/CONCERNS.md`]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| 向量索引与近似检索 | 自研 ANN 索引 | Qdrant 集合与 points API | 自研索引成本高且易错 [CITED: https://api.qdrant.tech/api-reference/points/upsert-points] |
| HTTP 入参校验 | 手写 if-else 大量分支 | Pydantic 模型 | 已是当前工程标准模式 [VERIFIED: `knowledge.py`, `files.py`] |
| 集合重建 API | 私有协议删除逻辑 | Qdrant 官方 delete/create | 官方接口语义明确、可维护 [CITED: Qdrant collections API] |

**Key insight:** Phase 1 的风险集中在“数据治理与可追溯”，不是底层向量引擎能力；优先复用现有基础设施并把预检/审计做实。

## Existing Implementation Patterns (Phase 1 直相关)

### 入库/存储适配
- `bid_tool_agents/backend/app/tools/database/qdrant.py`：已有 `create_collection`、`upsert`、`search`、`delete` 封装，可直接作为 writer 底座。 [VERIFIED]
- `bid_tool_agents/backend/app/tools/database/postgres.py`：已有全局初始化 + 表模型模式，可复用为审计持久化模式。 [VERIFIED]

### 向量写入
- 现有 `upsert(collection_name, points)` 已对接 `PointStruct` 写入路径。 [VERIFIED: `qdrant.py`]
- `PointId` 类型支持 `int | str | UUID`（字符串 ID 需谨慎约束格式）。 [CITED: https://python-client.qdrant.tech/_modules/qdrant_client/conversions/common_types]

### 批处理
- 代码库尚无成熟批量入库执行器（仅有 `calculate_batch_similarity` TODO）。 [VERIFIED: `similarity_calculation.py`]
- 结论：Phase 1 需要新增明确的“batch size + flush”实现，而非复用现有业务逻辑。 [VERIFIED]

### 审计记录
- 当前有任务记录模型 `TaskRecord` 可作为审计字段设计参考。 [VERIFIED: `postgres.py`]
- 目前没有法规入库审计实体，需在 Phase 1 新增。 [VERIFIED]

### 异常处理
- `files.py` 使用 `HTTPException` 做输入校验失败返回。 [VERIFIED]
- `agents.py` 使用 `try/except` 包装并返回结构化错误。 [VERIFIED]
- `pdf.py` 存在吞异常风险，提示 Phase 1 必须输出错误明细，不可 silent failure。 [VERIFIED: `.planning/codebase/CONCERNS.md`]

## Common Pitfalls

### Pitfall 1: 集合命名漂移
**What goes wrong:** 配置默认 `bid_documents`，需求要求 `laws_regulations`。  
**Why it happens:** `config.py` 默认值未与 Phase 目标对齐。  
**How to avoid:** Phase 1 明确以脚本参数或专用常量覆盖集合名。  
**Warning signs:** 入库成功但 API 查询不到法规数据。  
[VERIFIED: `config.py` + `knowledge.py` + `ROADMAP.md`]

### Pitfall 2: Qdrant 客户端命名冲突
**What goes wrong:** 本地类名与第三方类同名，可能递归构造或行为歧义。  
**Why it happens:** `qdrant.py` 同时 `from qdrant_client import QdrantClient` 且自定义 `class QdrantClient`。  
**How to avoid:** 重命名本地类（如 `QdrantStore`），第三方导入使用别名。  
**Warning signs:** 初始化时报错或卡死。  
[VERIFIED: `qdrant.py`][VERIFIED: `.planning/codebase/CONCERNS.md`]

### Pitfall 3: 未对 JSONL 做严格预检
**What goes wrong:** 部分脏行入库后很难追溯与回滚。  
**Why it happens:** 只做“能 parse 就写入”，没有字段完整性校验。  
**How to avoid:** D-15 强制必填字段校验并 fail-fast。  
**Warning signs:** 检索命中 payload 缺字段。  
[VERIFIED: `01-CONTEXT.md`]

## Recommended Implementation Strategy

1. **先修底座风险**：修复 `qdrant.py` 命名冲突并统一集合名来源。  
2. **构建可测试的入库域模块**：拆分 loader/chunker/vectorizer/writer/audit，避免脚本里堆逻辑。  
3. **落地 force 全量重建**：默认禁止删库，显式 `force=true` 才执行 delete/create。  
4. **实现批处理写入**：按 batch upsert，失败即中断并返回结构化错误。  
5. **补齐审计与测试**：输出摘要+错误明细，并对 INGEST-01~04 建最小测试闭环。

## Dependencies & Landing Order

| Order | Item | Type | Blocking | Notes |
|------|------|------|----------|-------|
| 1 | 修复 `qdrant.py` 命名冲突 | Code | Yes | 不修会影响所有写入路径 |
| 2 | 确认向量生成器接口（1536 维） | Code/Config | Yes | 当前仓库无法规入库专用 embedding 适配 |
| 3 | 新增入库域模块（loader/chunker/writer/audit） | Code | Yes | 主体实现 |
| 4 | 新增脚本入口 `ingest_laws.py` | Code | Yes | Phase 1 对外执行入口 |
| 5 | 增加入库测试与样例 | Test | High | 覆盖 INGEST-01~04 |

## Reusable Files

- `bid_tool_agents/backend/app/config.py`（配置模型、vector_db 参数源）  
- `bid_tool_agents/backend/app/tools/database/qdrant.py`（集合管理与 upsert 接口，需修复）  
- `bid_tool_agents/backend/app/api/v1/knowledge.py`（`laws_regulations` 类型定义，供 Phase 2 对齐）  
- `bid_tool_agents/backend/app/tools/database/postgres.py`（审计结构参考）  
- `bid_tool_agents/backend/tests/pytest.ini`（测试运行基线）

## Suggested New Files

- `bid_tool_agents/backend/app/domain/knowledge_ingest/models.py`
- `bid_tool_agents/backend/app/domain/knowledge_ingest/loader.py`
- `bid_tool_agents/backend/app/domain/knowledge_ingest/chunker.py`
- `bid_tool_agents/backend/app/domain/knowledge_ingest/vectorizer.py`
- `bid_tool_agents/backend/app/domain/knowledge_ingest/writer.py`
- `bid_tool_agents/backend/app/domain/knowledge_ingest/audit.py`
- `bid_tool_agents/backend/app/scripts/ingest_laws.py`
- `bid_tool_agents/backend/tests/knowledge_ingest/test_loader.py`
- `bid_tool_agents/backend/tests/knowledge_ingest/test_writer.py`
- `bid_tool_agents/backend/tests/knowledge_ingest/test_idempotent_rebuild.py`

## Open Questions (RESOLVED)

1. **Embedding 来源已锁定（RESOLVED）**
   - RESOLVED: Phase 1 通过新增 `vectorizer.py` 统一调用当前后端既有 LLM/向量能力，输出固定 `1536` 维向量；实现上采用“可替换 provider 适配层”，但对上游 writer 暴露统一接口，避免脚本直接耦合具体 provider。
   - Scope note: Phase 1 不扩展新模型路由功能，只要求稳定生成法规向量并可被测试替身替换。
   - Evidence: 与 D-07（固定 1536）一致，且与“脚本优先、底座优先”的 Phase 目标一致。
   - Tag: [RESOLVED]

2. **审计落地介质已锁定（RESOLVED）**
   - RESOLVED: Phase 1 采用本地结构化文件（JSONL）落地重建审计，至少记录：start/end time、input files、total/success/fail count、version、collection、force。
   - Scope note: 数据库持久化审计作为后续增强项，不阻塞 Phase 1 的 INGEST-04 验收。
   - Evidence: 与 D-12（必须结构化审计）和 D-13（脚本入口优先）一致。
   - Tag: [RESOLVED]

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python runtime | 入库脚本与测试执行 | ✗ | — | 无（阻塞） |
| pip | 安装/校验依赖 | ✗ | — | 无（阻塞） |
| pytest | Phase 1 自动化验证 | ✗ | — | 暂以人工 dry-run（不建议长期） |
| Docker CLI | 本地拉起 Qdrant（常见路径） | ✗ | — | 外部现成 Qdrant 实例 |
| qdrant CLI | 本机运维命令 | ✗ | — | 使用 HTTP API 或 Python client |

**Missing dependencies with no fallback:**
- Python/pip（当前机器无法直接执行 Phase 1 脚本与测试）

**Missing dependencies with fallback:**
- Docker/qdrant CLI 可由远端或已有服务替代，但需要可访问 Qdrant endpoint

## Validation Architecture

`workflow.nyquist_validation` 在 `.planning/config.json` 显式为 `false`，按约定跳过该节。 [VERIFIED: `.planning/config.json`]

## Security Domain

### Applicable ASVS Categories
| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | Phase 1 脚本模式，无用户认证面 |
| V3 Session Management | no | 同上 |
| V4 Access Control | yes | `force=true` 作为破坏性操作防护门槛（命令级） |
| V5 Input Validation | yes | JSON 解析 + 必填字段校验 + fail-fast |
| V6 Cryptography | yes | `chunk_id` 使用标准哈希库，不自研算法 [ASSUMED] |

### Known Threat Patterns for this phase
| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| 恶意/畸形 JSONL 输入 | Tampering | 严格 schema 校验，失败即终止 |
| 误触发全量删库 | Denial of Service | `force` 双保险 + 审计记录 |
| 元数据注入导致追溯污染 | Integrity | 仅白名单字段写入 payload，禁自由扩展 |

## Sources

### Primary (HIGH confidence)
- `d:/bid_management/ai_bid_management/.planning/phases/01-fa-gui-shu-ju-ru-ku-di-zuo/01-CONTEXT.md` - Phase 1 锁定决策  
- `d:/bid_management/ai_bid_management/.planning/REQUIREMENTS.md` - INGEST-01~04 定义  
- `d:/bid_management/ai_bid_management/.planning/ROADMAP.md` - Phase 1 范围与验收标准  
- `d:/bid_management/ai_bid_management/bid_tool_agents/backend/app/config.py` - 集合名与向量维度配置  
- `d:/bid_management/ai_bid_management/bid_tool_agents/backend/app/tools/database/qdrant.py` - 现有向量写入封装  
- `d:/bid_management/ai_bid_management/bid_tool_agents/backend/app/api/v1/knowledge.py` - knowledge type 约束  
- `d:/bid_management/ai_bid_management/docs/dataset/zhaobiao-toubiao/README.md` 与两份 JSONL 样本 - 输入数据形态  

### Secondary (MEDIUM confidence)
- [Qdrant Delete Collection API](https://api.qdrant.tech/api-reference/collections/delete-collection) - 删集合语义  
- [Qdrant Create Collection API](https://api.qdrant.tech/api-reference/collections/create-collection) - 建集合参数  
- [Qdrant Upsert Points API](https://api.qdrant.tech/api-reference/points/upsert-points) - upsert 行为  

### Tertiary (LOW confidence)
- [Qdrant Python common types](https://python-client.qdrant.tech/_modules/qdrant_client/conversions/common_types) - PointId 类型别名（文档站源码页）

## Metadata

**Confidence breakdown:**
- Standard stack: MEDIUM - 版本来自仓库声明，未在本机运行时验证  
- Architecture: HIGH - 受 CONTEXT 锁定决策约束清晰  
- Pitfalls: HIGH - 由仓库现状与 concerns 文档直接支撑

**Research date:** 2026-04-20  
**Valid until:** 2026-05-20

## RESEARCH COMPLETE
