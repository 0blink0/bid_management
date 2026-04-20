# 02-02 Summary

## Outcome

完成法规重建异步任务链路，支持触发重建并通过任务状态接口轮询收敛。

## Delivered

- 新增任务管理模块：`app/domain/knowledge_ingest/tasks.py`。
- 落地 `POST /api/v1/knowledge/ingest/rebuild`，返回 `task_id/status_url/request_id`（202）。
- 落地 `GET /api/v1/knowledge/tasks/{task_id}`，返回 queued/running/succeeded/failed 状态快照。
- 任务失败时输出统一错误结构，并带 `retryable` 判定。
- 新增 API 回归测试：`tests/api/test_knowledge_ingest_api.py`。

## Verification

- `pytest tests/api/test_knowledge_ingest_api.py -q`
- 结果：通过
