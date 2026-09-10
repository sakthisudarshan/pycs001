"""
Pydantic models — mirrors RecordModel.cs
Covers: All Definition Coverage (Beniget), pyflakes, Statement Coverage
"""
from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field


class RecordModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    title: str = ""
    description: str = ""
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    model_config = {"populate_by_name": True}


class CreateRecordDto(BaseModel):
    title: str
    description: str
