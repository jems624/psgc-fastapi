import logging

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.db.models import Location
from app.schemas.locations import LocationResponse, LocationsResponse
from app.crud import city, barangay
from app.constants import GeoLevels

router = APIRouter(tags=["Municipalities"])


@router.get("/")
async def get_municipalities(db: Annotated[Session, Depends(get_db)]) -> LocationsResponse:
    try:
        rows = city.get_all(db, geo_levels=[GeoLevels.Municipality])
        return LocationsResponse(
            regions=[
                LocationResponse(
                    code=row.code,
                    name=row.name
                )
                for row in rows
            ]
        )

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/{municipality_code}")
async def get_municipality(municipality_code: str, db: Annotated[Session, Depends(get_db)]) -> LocationResponse:
    try:
        record = city.get(db, municipality_code, geo_levels=[GeoLevels.Municipality])

        if record is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Municipality not found")

        return LocationResponse(
            code=record.code,
            name=record.name
        )

    except HTTPException as e:
        raise e

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/{municipality_code}/barangays")
async def get_municipality_barangays(municipality_code: str, db: Annotated[Session, Depends(get_db)]) -> LocationsResponse:
    try:
        record = city.get(db, municipality_code, geo_levels=[GeoLevels.Municipality])

        if record is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Municipality not found")

        rows = barangay.get_all(db, city_code=municipality_code)
        return LocationsResponse(
            regions=[
                LocationResponse(
                    code=row.code,
                    name=row.name
                )
                for row in rows
            ]
        )

    except HTTPException as e:
        raise e

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)