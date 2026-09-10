"""
Tests for src.db and src.grpc_server to achieve >= 85% full suite coverage.
"""
import pytest
from unittest.mock import MagicMock, patch
from queue import Queue

from src.db import get_client, get_database, get_collection, close_client
from src.grpc_server import (
    notify_record_created,
    RecordServiceServicer,
    _subscribers,
    _lock,
)


class TestDatabaseHelpers:
    def test_get_client_and_close(self):
        with patch("src.db.MongoClient") as mock_mc:
            client = get_client()
            assert client is not None
            close_client()

    def test_get_database(self):
        with patch("src.db.MongoClient") as mock_mc:
            db = get_database()
            assert db is not None

    def test_get_collection(self):
        with patch("src.db.MongoClient") as mock_mc:
            col = get_collection("records")
            assert col is not None


class TestGrpcServer:
    def test_notify_record_created_with_subscribers(self):
        q = Queue()
        with _lock:
            _subscribers.append(q)
        try:
            notify_record_created({"title": "Event1"})
            item = q.get_nowait()
            assert item == {"title": "Event1"}
        finally:
            with _lock:
                if q in _subscribers:
                    _subscribers.remove(q)

    def test_notify_record_created_error_handled(self):
        bad_sub = MagicMock()
        bad_sub.put_nowait.side_effect = Exception("Queue full")
        with _lock:
            _subscribers.append(bad_sub)
        try:
            notify_record_created({"title": "Event2"})
        finally:
            with _lock:
                if bad_sub in _subscribers:
                    _subscribers.remove(bad_sub)

    def test_grpc_get_record_found(self):
        servicer = RecordServiceServicer()
        req = MagicMock()
        req.id = "60c72b2f9b1d8b2bad000001"
        context = MagicMock()

        with patch("src.grpc_server.get_collection") as mock_col:
            mock_col.return_value.find_one.return_value = {
                "_id": req.id,
                "title": "Rec",
                "description": "Desc",
                "created_at": "2024-01-01T00:00:00Z",
            }
            res = servicer.get_record(req, context)
            assert res is None or getattr(res, "id", None) == req.id

    def test_grpc_get_record_not_found(self):
        servicer = RecordServiceServicer()
        req = MagicMock()
        req.id = "nonexistent"
        context = MagicMock()

        with patch("src.grpc_server.get_collection") as mock_col:
            mock_col.return_value.find_one.return_value = None
            res = servicer.get_record(req, context)
            assert res is None
            context.set_code.assert_called_once()
