# Phase 2: 法规知识库 API - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-20
**Phase:** 02-法规知识库 API
**Areas discussed:** API 契约, 检索行为, 错误模型, 执行模式

---

## API 契约

| Option | Description | Selected |
|--------|-------------|----------|
| `POST /knowledge/ingest/rebuild` | 显式重建语义，接口职责清晰 | ✓ |
| `POST /knowledge/ingest` | 统一入口，通过参数区分模式 | |
| 两者都保留 | 兼容性强但维护成本更高 | |

| Option | Description | Selected |
|--------|-------------|----------|
| `POST /knowledge/query` | body 传查询参数，扩展性更好 | ✓ |
| `GET /knowledge/search` | URL 参数简洁，但扩展受限 | |
| 两者都支持 | 双契约维护成本较高 | |

| Option | Description | Selected |
|--------|-------------|----------|
| 固定结构 `items+total+took_ms+trace` | Agent 消费最稳定 | ✓ |
| 仅 `items[]` | 结构简单但诊断信息少 | |
| verbose 调试字段 | 排障方便但响应噪声大 | |

| Option | Description | Selected |
|--------|-------------|----------|
| `title/chapter/source_file/chunk_id/score` | 最小追溯集合 | |
| 上述 + `version` | 追溯完整性更高 | ✓ |
| payload 全字段 | 最全但冗余 | |

---

## 检索行为

| Option | Description | Selected |
|--------|-------------|----------|
| 默认 `laws_regulations` | 与本期范围一致 | ✓ |
| 必须显式传 `knowledge_type` | 强约束 | |
| 默认全类型搜索 | 范围过大 | |

| Option | Description | Selected |
|--------|-------------|----------|
| 默认10，最大50，超限截断 | 稳定且实用 | ✓ |
| 默认5，最大20 | 更保守 | |
| 超限直接报错 | 更严格 | |

| Option | Description | Selected |
|--------|-------------|----------|
| score 降序 + float 分值 | 标准检索行为 | ✓ |
| score 降序 + 四位小数 | 展示友好 | |
| 业务加权排序 | 超出本期最小范围 | |

---

## 错误模型

| Option | Description | Selected |
|--------|-------------|----------|
| 422 | 参数校验语义清晰 | ✓ |
| 400 | 通用但信息粒度弱 | |
| 200 + 错误码 | 不推荐 | |

| Option | Description | Selected |
|--------|-------------|----------|
| 503 + `retryable=true` | 依赖故障可重试语义明确 | ✓ |
| 500 | 通用内部错误 | |
| 424 | 语义明确但生态不常用 | |

| Option | Description | Selected |
|--------|-------------|----------|
| `error_code/message/details/request_id` | 统一且可诊断 | ✓ |
| 仅 `message` | 过于简化 | |
| 堆栈输出 | 仅适合调试环境 | |

---

## 执行模式

| Option | Description | Selected |
|--------|-------------|----------|
| 异步任务 + task_id | 避免超时，便于编排 | ✓ |
| 同步阻塞 | 实现简单但超时风险高 | |
| sync/async 双模式 | 灵活但复杂 | |

| Option | Description | Selected |
|--------|-------------|----------|
| `GET /knowledge/tasks/{task_id}` | REST 语义清晰 | ✓ |
| `POST /knowledge/tasks/query` | 兼容复杂条件 | |
| 不提供任务查询接口 | 可用性不足 | |

---

## Claude's Discretion

- 任务状态存储介质与生命周期清理策略留待实现阶段确定。
- `trace` 结构的字段深度由实现阶段结合现有日志规范确定。

## Deferred Ideas

- 全知识库类型统一检索
- 业务加权重排与复杂排序策略
