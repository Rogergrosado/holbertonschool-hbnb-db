from datetime import datetime
from typing import Any, Optional
from uuid import uuid4
from abc import ABC, abstractmethod
from sqlalchemy import DateTime, String, Column
from sqlalchemy.sql import func
from src import db

class Base(db.Model):

    __abstract__ = True
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(
        self,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        **kwargs,
    ) -> None:
        if kwargs:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    continue
                setattr(self, key, value)

        self.id = id or str(uuid4())
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    @classmethod
    def get(cls, id) -> "Any | None":
        from src.persistence import db

        return db.get(cls.__name__.lower(), id)

    @classmethod
    def get_all(cls) -> list["Any"]:
        from src.persistence import db

        return db.get_all(cls.__name__.lower())

    @classmethod
    def delete(cls, id) -> bool:
        from src.persistence import db

        obj = cls.get(id)

        if not obj:
            return False

        return db.delete(obj)

    @abstractmethod
    def to_dict(self) -> dict: ...

    @staticmethod
    @abstractmethod
    def create(data: dict) -> Any: ...

    @staticmethod
    @abstractmethod
    def update(entity_id: str, data: dict) -> Any | None: ...
