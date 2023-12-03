from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.base import CRUDLocation
from app.db.models import Location
from app.constants import GeoLevels

class CRUDBarangay(CRUDLocation):

    def get_all(
        self,
        db: Session,
        region_code: str | None = None,
        province_code: str | None = None,
        city_code: str | None = None
    ) -> Sequence[Location]:
        stmt = select(Location).where(Location.geo_level == GeoLevels.Barangay.value)
        if region_code is not None:
            stmt = stmt.where(Location.region == region_code)

        if province_code is not None:
            stmt = stmt.where(Location.province == province_code)

        if city_code is not None:
            stmt = stmt.where(Location.city_municipality == city_code)

        return db.scalars(stmt).all()


barangay = CRUDBarangay(Location)