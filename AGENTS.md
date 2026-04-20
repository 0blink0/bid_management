# GSD Project Guide

## Project

- Name: 智能招投标审查平台（法律法规知识库专项）
- Scope now: 构建 `laws_regulations` 知识库及 API（非完整生成式 RAG）

## Working Agreements

- Data source: 使用 `docs/dataset/zhaobiao-toubiao` 下不标记版 JSONL
- Naming: 知识库类型与集合命名对齐 `laws_regulations`
- API-first: 优先提供稳定的入库/检索接口，供 Agent 复用
- Traceability: 检索结果必须包含可追溯元数据

## Phase Flow

1. `/gsd-discuss-phase 1`
2. `/gsd-plan-phase 1`
3. `/gsd-execute-phase 1`

## Phase 1 Focus

- 法规数据解析与标准化
- 向量化写入 Qdrant
- 元数据建模与幂等重建
