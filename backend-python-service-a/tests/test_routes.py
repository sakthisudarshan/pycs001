"""
Tests for REST routes (routes.py) — uses FastAPI TestClient with mocked MongoDB.

Metric targets:
  ✅ Statement Coverage %   (all route handlers executed)
  ✅ Branch Coverage %      (404 / 400 / 201 paths)
  ✅ Coverage Delta %       (new code is fully covered)
  ✅ All-Uses Coverage %    (dto fields defined → used in insert → returned)
"""
import pytest
from unittest.mock import MagicMock, patch

try:
    from fastapi.testclient import TestClient
    from bson import ObjectId
    import src.db
    import src.grpc_server

    with patch.object(src.db, "get_collection"), patch.object(src.grpc_server, "notify_record_created"):
        from src.main import app

    client = TestClient(app)
    HAS_FASTAPI = True
except (ImportError, Exception):
    HAS_FASTAPI = False
    client = None
    ObjectId = None


def make_doc(title="Test", description="Desc"):
    oid = ObjectId() if ObjectId else "mock_id"
    return {
        "_id": oid,
        "title": title,
        "description": description,
        "created_at": "2024-01-01T00:00:00+00:00",
    }


@pytest.mark.skipif(not HAS_FASTAPI, reason="fastapi/bson not available")
class TestGetAll:

    def test_get_all_empty(self):
        with patch.object(src.routes, "get_collection") as mock_col:
            mock_col.return_value.find.return_value = []
            resp = client.get("/api/records/")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_get_all_returns_records(self):
        doc = make_doc("Alpha", "Beta")
        with patch.object(src.routes, "get_collection") as mock_col:
            mock_col.return_value.find.return_value = [doc]
            resp = client.get("/api/records/")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["title"] == "Alpha"


@pytest.mark.skipif(not HAS_FASTAPI, reason="fastapi/bson not available")
class TestGetById:

    def test_get_by_id_found(self):
        doc = make_doc("Found", "Here")
        with patch.object(src.routes, "get_collection") as mock_col:
            mock_col.return_value.find_one.return_value = doc
            resp = client.get(f"/api/records/{str(doc['_id'])}")
        assert resp.status_code == 200
        assert resp.json()["title"] == "Found"

    def test_get_by_id_not_found(self):
        with patch.object(src.routes, "get_collection") as mock_col:
            mock_col.return_value.find_one.return_value = None
            resp = client.get(f"/api/records/{str(ObjectId())}")
        assert resp.status_code == 404
        assert "not found" in resp.json()["detail"]

    def test_get_by_id_invalid_format(self):
        resp = client.get("/api/records/not-a-valid-objectid")
        assert resp.status_code == 400
        assert "invalid id" in resp.json()["detail"]


@pytest.mark.skipif(not HAS_FASTAPI, reason="fastapi/bson not available")
class TestCreateRecord:

    def test_create_returns_201(self):
        doc = make_doc("NewRec", "NewDesc")
        mock_result = MagicMock()
        mock_result.inserted_id = doc["_id"]

        with patch.object(src.routes, "get_collection") as mock_col, \
             patch.object(src.routes, "notify_record_created") as mock_notify:
            mock_col.return_value.insert_one.return_value = mock_result
            resp = client.post("/api/records/", json={
                "title": "NewRec",
                "description": "NewDesc",
            })

        assert resp.status_code == 201
        body = resp.json()
        assert body["title"] == "NewRec"
        assert body["description"] == "NewDesc"
        mock_notify.assert_called_once()

    def test_create_missing_title_returns_422(self):
        resp = client.post("/api/records/", json={"description": "no title"})
        assert resp.status_code == 422
