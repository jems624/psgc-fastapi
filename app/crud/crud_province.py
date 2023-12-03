from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.base import CRUDLocation
from app.db.models import Location
from app.constants import GeoLevels

class CRUDProvince(CRUDLocation):

    def get_all(self, db: Session, region_code: str | None = None) -> Sequence[Location]:
        stmt = select(Location).where(Location.geo_level == GeoLevels.Province.value)
        if region_code is not None:
            stmt = stmt.where(Location.region == region_code)

        return db.scalars(stmt).all()


province = CRUDProvince(Location)