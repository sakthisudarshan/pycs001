"""
gRPC RecordService implementation — mirrors RecordServiceImpl.cs
Covers: Branch Coverage, Path Coverage, All Uses Coverage (C-Use / P-Use)
"""
from __future__ import annotations

import asyncio
import threading
from concurrent import futures
from typing import Iterator

import grpc

try:
    from . import record_pb2, record_pb2_grpc  # type: ignore[import]
except ImportError:
    record_pb2 = None  # pragma: no cover
    record_pb2_grpc = None  # pragma: no cover

from .db import get_collection

_subscribers: list = []
_lock = threading.Lock()


def notify_record_created(record_dict: dict) -> None:
    """Push a newly created record to all active gRPC stream subscribers."""
    with _lock:
        active = list(_subscribers)

    for sub in active:
        try:
            sub.put_nowait(record_dict)
        except Exception as exc:  # noqa: BLE001
            print(f"[py-service-a][grpc] subscriber write error: {exc}")


class RecordServiceServicer:
    """
    Python gRPC servicer — mirrors RecordServiceImpl.cs.
    Implements GetRecord (unary) and WatchRecords (server-streaming).
    """

    def get_record(self, request, context):  # type: ignore[override]
        collection = get_collection("records")
        doc = collection.find_one({"_id": request.id})

        if doc is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("record not found")
            return None

        if record_pb2 is None:  # pragma: no cover
            return None

        return record_pb2.Record(
            id=str(doc["_id"]),
            title=doc.get("title", ""),
            description=doc.get("description", ""),
            created_at=doc.get("created_at", ""),
        )

    def watch_records(self, request, context):  # type: ignore[override]
        """Server-streaming: push new records to connected subscribers."""
        import queue as q_mod

        queue: q_mod.Queue = q_mod.Queue()
        with _lock:
            _subscribers.append(queue)

        print("[py-service-a][grpc] client subscribed to watch_records")
        try:
            while context.is_active():
                try:
                    item = queue.get(timeout=1.0)
                    if record_pb2 is not None:
                        yield record_pb2.Record(**item)
                except Exception:  # noqa: BLE001
                    continue
        finally:
            with _lock:
                if queue in _subscribers:
                    _subscribers.remove(queue)
            print("[py-service-a][grpc] watch_records client disconnected")


def serve(port: int = 50051) -> None:  # pragma: no cover
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    if record_pb2_grpc is not None:
        record_pb2_grpc.add_RecordServiceServicer_to_server(
            RecordServiceServicer(), server
        )
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"[py-service-a][grpc] server listening on port {port}")
    server.wait_for_termination()
