# Requirements: 智能招投标审查平台（法律法规知识库专项）

**Defined:** 2026-04-20
**Core Value:** 在招投标审查场景下，系统能够稳定返回准确且可定位到法条原文的法规检索结果

## v1 Requirements

### Data Ingestion

- [x] **INGEST-01**: 系统可从不标记版 JSONL 读取法规数据并完成结构化解析
- [x] **INGEST-02**: 系统可将法条内容向量化并写入 `laws_regulations` 集合
- [x] **INGEST-03**: 系统可为每条法规保存完整元数据（`title`、`chapter`、`source_file`、`chunk_id`、`version`）
- [x] **INGEST-04**: 系统支持幂等重建（重复执行入库不会产生不可控重复数据）

### Knowledge API

- [x] **KAPI-01**: 用户可通过 API 触发法规知识库导入任务
- [x] **KAPI-02**: 用户可通过 API 执行法规语义检索并限定返回条数
- [x] **KAPI-03**: API 检索结果返回命中分数及可追溯元数据
- [x] **KAPI-04**: API 支持按知识库类型过滤，默认使用 `laws_regulations`

### Quality Baseline

- [x] **QUAL-01**: 系统具备基础检索评测样例集与离线评估入口
- [x] **QUAL-02**: 关键指标可输出（Recall@5、MRR、响应时延）
- [x] **QUAL-03**: 检索失败或数据异常时，API 返回明确错误信息

## v2 Requirements

### Retrieval Enhancement

- **RETR-01**: 引入重排模型提升法规条文排序质量
- **RETR-02**: 支持多路召回（向量 + 关键词）混合检索

### Generation and Graph

- **RAG-01**: 基于检索证据生成结构化回答并附引用
- **GRAPH-01**: 建立法规知识图谱并支持图谱增强检索

## Out of Scope

| Feature | Reason |
|---------|--------|
| 完整生成式问答链路 | 本期优先确保知识库检索基础稳定 |
| 法规图谱构建与图谱推理 | 依赖后续实体/关系建模与数据治理 |
| 非法规类知识库统一重构 | 本期限定 `laws_regulations`，降低范围风险 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| INGEST-01 | Phase 1 | Completed |
| INGEST-02 | Phase 1 | Completed |
| INGEST-03 | Phase 1 | Completed |
| INGEST-04 | Phase 1 | Completed |
| KAPI-01 | Phase 2 | Completed |
| KAPI-02 | Phase 2 | Completed |
| KAPI-03 | Phase 2 | Completed |
| KAPI-04 | Phase 2 | Completed |
| QUAL-01 | Phase 3 | Completed |
| QUAL-02 | Phase 3 | Completed |
| QUAL-03 | Phase 3 | Completed |

**Coverage:**
- v1 requirements: 11 total
- Mapped to phases: 11
- Unmapped: 0

---
*Requirements defined: 2026-04-20*
*Last updated: 2026-04-20 after initial definition*
