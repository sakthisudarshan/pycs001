"""
REST API routes — mirrors RecordsController.cs
GET  /records        → list all records
GET  /records/{id}  → get by id
POST /records        → create record

Covers: Statement Coverage, Branch Coverage, Coverage Delta, All Uses
"""
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from bson import ObjectId
from bson.errors import InvalidId

from .db import get_collection
from .models import CreateRecordDto, RecordModel
from .grpc_server import notify_record_created

router = APIRouter(prefix="/api/records", tags=["records"])


def _doc_to_model(doc: dict) -> RecordModel:
    """Convert a MongoDB document to a RecordModel."""
    return RecordModel(
        id=str(doc["_id"]),
        title=doc.get("title", ""),
        description=doc.get("description", ""),
        created_at=doc.get("created_at", ""),
    )


@router.get("/", response_model=list[RecordModel])
def get_all():
    """Return all records from MongoDB."""
    collection = get_collection("records")
    docs = list(collection.find())
    return [_doc_to_model(d) for d in docs]


@router.get("/{record_id}", response_model=RecordModel)
def get_by_id(record_id: str):
    """Return a single record by ObjectId string."""
    collection = get_collection("records")

    try:
        oid = ObjectId(record_id)
    except (InvalidId, Exception):
        raise HTTPException(status_code=400, detail="invalid id format")

    doc = collection.find_one({"_id": oid})
    if doc is None:
        raise HTTPException(status_code=404, detail="record not found")

    return _doc_to_model(doc)


@router.post("/", response_model=RecordModel, status_code=201)
def create_record(dto: CreateRecordDto):
    """Insert a new record and notify gRPC subscribers."""
    collection = get_collection("records")

    now = datetime.now(timezone.utc).isoformat()
    doc = {
        "title": dto.title,
        "description": dto.description,
        "created_at": now,
    }

    result = collection.insert_one(doc)
    doc["_id"] = result.inserted_id

    model = _doc_to_model(doc)

    notify_record_created(
        {
            "id": model.id or "",
            "title": model.title,
            "description": model.description,
            "created_at": model.created_at,
        }
    )

    return model
