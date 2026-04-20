from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import create_app


def _client() -> TestClient:
    return TestClient(create_app())


def test_default_knowledge_type(monkeypatch):
    captured = {}

    class DummyStore:
        def search(self, collection_name, query_vector, limit, score_threshold=None):
            captured["collection_name"] = collection_name
            captured["limit"] = limit
            return []

    monkeypatch.setattr("app.api.v1.knowledge.get_qdrant", lambda: DummyStore())
    monkeypatch.setattr("app.api.v1.knowledge.vectorizer.embed_chunks", lambda chunks: [[0.1] * 1536])

    resp = _client().post("/api/v1/knowledge/query", json={"query": "招标法"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["trace"]["knowledge_type"] == "laws_regulations"
    assert body["trace"]["limit"] == 10
    assert captured["collection_name"] == "laws_regulations"
    assert captured["limit"] == 10


def test_limit_clamp(monkeypatch):
    captured = {}

    class DummyStore:
        def search(self, collection_name, query_vector, limit, score_threshold=None):
            captured["limit"] = limit
            return []

    monkeypatch.setattr("app.api.v1.knowledge.get_qdrant", lambda: DummyStore())
    monkeypatch.setattr("app.api.v1.knowledge.vectorizer.embed_chunks", lambda chunks: [[0.1] * 1536])

    resp = _client().post("/api/v1/knowledge/query", json={"query": "招标法", "limit": 200})
    assert resp.status_code == 200
    assert resp.json()["trace"]["limit"] == 50
    assert captured["limit"] == 50


def test_validation_422():
    resp = _client().post("/api/v1/knowledge/query", json={"knowledge_type": "laws_regulations"})
    assert resp.status_code == 422
    body = resp.json()
    assert set(body.keys()) == {"error_code", "message", "details", "request_id"}


def test_score_desc(monkeypatch):
    class DummyStore:
        def search(self, collection_name, query_vector, limit, score_threshold=None):
            return [
                {"id": "a", "score": 0.2, "payload": {"title": "A", "chapter": "c1", "source_file": "s1", "chunk_id": "a", "version": "v1"}},
                {"id": "b", "score": 0.9, "payload": {"title": "B", "chapter": "c2", "source_file": "s2", "chunk_id": "b", "version": "v1"}},
            ]

    monkeypatch.setattr("app.api.v1.knowledge.get_qdrant", lambda: DummyStore())
    monkeypatch.setattr("app.api.v1.knowledge.vectorizer.embed_chunks", lambda chunks: [[0.1] * 1536])
    resp = _client().post("/api/v1/knowledge/query", json={"query": "招标法"})
    assert resp.status_code == 200
    items = resp.json()["items"]
    assert [i["chunk_id"] for i in items] == ["b", "a"]


def test_dependency_failure_503(monkeypatch):
    def _raise(_chunks):
        raise RuntimeError("qdrant unavailable")

    monkeypatch.setattr("app.api.v1.knowledge.vectorizer.embed_chunks", _raise)
    resp = _client().post("/api/v1/knowledge/query", json={"query": "招标法"})
    assert resp.status_code == 503
    body = resp.json()
    assert body["error_code"] == "KNOWLEDGE_QUERY_DEPENDENCY_ERROR"
    assert body["message"] == "knowledge query dependency failed"
    assert isinstance(body["request_id"], str) and body["request_id"]
    assert body["details"]["retryable"] is True
    assert set(body.keys()) == {"error_code", "message", "details", "request_id"}


def test_error_contract_details_on_validation_422():
    resp = _client().post("/api/v1/knowledge/query", json={"query": ""})
    assert resp.status_code == 422
    body = resp.json()
    assert body["error_code"] == "VALIDATION_ERROR"
    assert body["message"] == "request payload validation failed"
    assert isinstance(body["request_id"], str) and body["request_id"]
    assert "validation_errors" in body["details"]


def test_response_shape(monkeypatch):
    class DummyStore:
        def search(self, collection_name, query_vector, limit, score_threshold=None):
            return [
                {
                    "id": "x1",
                    "score": 0.5,
                    "payload": {
                        "title": "标题",
                        "chapter": "第一章",
                        "source_file": "docs/a.jsonl",
                        "chunk_id": "x1",
                        "version": "2026-04-20",
                    },
                }
            ]

    monkeypatch.setattr("app.api.v1.knowledge.get_qdrant", lambda: DummyStore())
    monkeypatch.setattr("app.api.v1.knowledge.vectorizer.embed_chunks", lambda chunks: [[0.1] * 1536])
    resp = _client().post("/api/v1/knowledge/query", json={"query": "招标法"})
    assert resp.status_code == 200
    body = resp.json()
    assert set(body.keys()) == {"items", "total", "took_ms", "trace"}
    assert body["total"] == len(body["items"])
    assert body["took_ms"] >= 0
    item = body["items"][0]
    for key in ("title", "chapter", "source_file", "chunk_id", "version", "score"):
        assert key in item
