from __future__ import annotations

import time
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import create_app


def _client() -> TestClient:
    return TestClient(create_app())


def _write_jsonl(path: Path):
    path.write_text('{"title":"招标投标法","chapter":"第一章","content":"第一条 为了规范招标投标活动。"}\n', encoding="utf-8")


def test_task_create(monkeypatch, tmp_path):
    monkeypatch.setattr("app.api.v1.knowledge.get_qdrant", lambda: object())
    fp = tmp_path / "laws.jsonl"
    _write_jsonl(fp)
    resp = _client().post("/api/v1/knowledge/ingest/rebuild", json={"input_paths": [str(fp)], "version": "v1", "force": True})
    assert resp.status_code == 202
    body = resp.json()
    assert "task_id" in body


def test_task_success_state(monkeypatch, tmp_path):
    class DummyStore:
        def delete_collection(self, collection_name):  # noqa: ARG002
            return True

        def create_collection(self, collection_name, vector_size=1536):  # noqa: ARG002
            return True

        def upsert(self, collection_name, points):  # noqa: ARG002
            return True

    monkeypatch.setattr("app.api.v1.knowledge.get_qdrant", lambda: DummyStore())
    monkeypatch.setattr("app.domain.knowledge_ingest.tasks.get_qdrant", lambda: DummyStore())
    monkeypatch.setattr("app.domain.knowledge_ingest.writer.embed_chunks", lambda chunks: [[0.1] * 1536 for _ in chunks])

    fp = tmp_path / "laws.jsonl"
    _write_jsonl(fp)
    audit = tmp_path / "audit.log"
    client = _client()
    created = client.post(
        "/api/v1/knowledge/ingest/rebuild",
        json={"input_paths": [str(fp)], "version": "v1", "force": True, "audit_path": str(audit)},
    )
    assert created.status_code == 202
    task_id = created.json()["task_id"]
    for _ in range(20):
        status_resp = client.get(f"/api/v1/knowledge/tasks/{task_id}")
        if status_resp.status_code == 200 and status_resp.json()["status"] in {"succeeded", "failed"}:
            break
        time.sleep(0.05)

    body = client.get(f"/api/v1/knowledge/tasks/{task_id}").json()
    assert body["status"] == "succeeded"
    assert body["summary"]["success"] >= 1


def test_task_failed_state(monkeypatch, tmp_path):
    def _raise(*args, **kwargs):  # noqa: ARG001
        raise RuntimeError("qdrant unavailable")

    monkeypatch.setattr("app.domain.knowledge_ingest.tasks.get_qdrant", _raise)

    fp = tmp_path / "laws.jsonl"
    _write_jsonl(fp)
    client = _client()
    created = client.post("/api/v1/knowledge/ingest/rebuild", json={"input_paths": [str(fp)], "version": "v1", "force": True})
    task_id = created.json()["task_id"]

    for _ in range(20):
        status_resp = client.get(f"/api/v1/knowledge/tasks/{task_id}")
        if status_resp.status_code in {503, 200} and status_resp.json()["status"] == "failed":
            break
        time.sleep(0.05)

    status_resp = client.get(f"/api/v1/knowledge/tasks/{task_id}")
    assert status_resp.status_code == 503
    body = status_resp.json()
    assert body["status"] == "failed"
    assert body["error"]["details"]["retryable"] is True


def test_ingest_rebuild_accepted(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "app.api.v1.knowledge.create_rebuild_task",
        lambda **kwargs: {"task_id": "t1", "status": "queued", "request_id": kwargs["request_id"]},
    )
    fp = tmp_path / "laws.jsonl"
    _write_jsonl(fp)
    resp = _client().post("/api/v1/knowledge/ingest/rebuild", json={"input_paths": [str(fp)], "version": "v2", "force": True})
    assert resp.status_code == 202
    body = resp.json()
    assert body["task_id"] == "t1"
    assert "/api/v1/knowledge/tasks/t1" in body["status_url"]


def test_task_status_query(monkeypatch):
    monkeypatch.setattr(
        "app.api.v1.knowledge.get_task_status",
        lambda task_id: {  # noqa: ARG005
            "task_id": "abc",
            "status": "running",
            "knowledge_type": "laws_regulations",
            "started_at": "2026-04-20T00:00:00Z",
            "updated_at": "2026-04-20T00:00:01Z",
            "summary": None,
            "error": None,
            "request_id": "r1",
        },
    )
    resp = _client().get("/api/v1/knowledge/tasks/abc")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "running"
    assert body["task_id"] == "abc"


def test_task_not_found(monkeypatch):
    monkeypatch.setattr("app.api.v1.knowledge.get_task_status", lambda task_id: None)  # noqa: ARG005
    resp = _client().get("/api/v1/knowledge/tasks/missing")
    assert resp.status_code == 404
    body = resp.json()
    assert set(body.keys()) == {"error_code", "message", "details", "request_id"}


def test_dependency_failure_503(monkeypatch, tmp_path):
    def _raise(**kwargs):  # noqa: ARG001
        raise RuntimeError("dependency failure")

    monkeypatch.setattr("app.api.v1.knowledge.create_rebuild_task", _raise)
    fp = tmp_path / "laws.jsonl"
    _write_jsonl(fp)
    resp = _client().post("/api/v1/knowledge/ingest/rebuild", json={"input_paths": [str(fp)], "version": "v1", "force": True})
    assert resp.status_code == 503
    body = resp.json()
    assert body["details"]["retryable"] is True
