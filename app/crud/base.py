from typing import Generic, TypeVar, Type, Any
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.models import Location

ModelType = TypeVar("ModelType", bound=Any)

class CRUDBase(Generic[ModelType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model


class CRUDLocation(CRUDBase[Location]):

    def get(self, db: Session, code: str) -> Location | None:
        return db.scalars(select(Location).where(Location.code == code)).one_or_none()
