from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.base import CRUDLocation
from app.db.models import Location
from app.constants import GeoLevels

class CRUDCity(CRUDLocation):

    def get_all(
        self,
        db: Session,
        region_code: str | None = None,
        province_code: str | None = None,
        geo_levels: list[GeoLevels] = [GeoLevels.City, GeoLevels.Municipality],
    ) -> Sequence[Location]:
        stmt = select(Location).where(Location.geo_level.in_([level.value for level in geo_levels]))
        if region_code is not None:
            stmt = stmt.where(Location.region == region_code)

        if province_code is not None:
            stmt = stmt.where(Location.province == province_code)

        return db.scalars(stmt).all()

    def get(
        self,
        db: Session, code: str,
        geo_levels: list[GeoLevels] = [GeoLevels.City, GeoLevels.Municipality],
    ) -> Location | None:
        return db.scalars(select(Location) \
            .where(Location.code == code) \
            .where(Location.geo_level.in_([level.value for level in geo_levels]))) \
            .one_or_none()


city = CRUDCity(Location)