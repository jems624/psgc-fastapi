from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.base import CRUDLocation
from app.db.models import Location
from app.constants import GeoLevels

class CRUDRegion(CRUDLocation):

    def get_all(self, db: Session) -> Sequence[Location]:
        return db.scalars(select(Location).where(Location.geo_level == GeoLevels.Region.value)).all()


region = CRUDRegion(Location)