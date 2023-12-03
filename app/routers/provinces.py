import logging

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.db.models import Location
from app.schemas.locations import LocationResponse, LocationsResponse
from app.crud import province, city, barangay
from app.constants import GeoLevels

router = APIRouter(tags=["Provinces"])


@router.get("/")
async def get_provinces(db: Annotated[Session, Depends(get_db)]) -> LocationsResponse:
    try:
        rows = province.get_all(db)
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

@router.get("/{province_code}")
async def get_province(province_code: str, db: Annotated[Session, Depends(get_db)]) -> LocationResponse:
    try:
        record = province.get(db, province_code)

        if record is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Province not found")

        return LocationResponse(
            code=record.code,
            name=record.name
        )

    except HTTPException as e:
        raise e

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/{province_code}/cities")
async def get_province_cities(province_code: str, db: Annotated[Session, Depends(get_db)]) -> LocationsResponse:
    try:
        record = province.get(db, province_code)

        if record is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Province not found")

        rows = city.get_all(db, province_code=province_code, geo_levels=[GeoLevels.City])
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

@router.get("/{province_code}/municipalities")
async def get_province_municipalities(province_code: str, db: Annotated[Session, Depends(get_db)]) -> LocationsResponse:
    try:
        record = province.get(db, province_code)

        if record is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Province not found")

        rows = city.get_all(db, province_code=province_code, geo_levels=[GeoLevels.Municipality])
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

@router.get("/{province_code}/cities-municipalities")
async def get_province_cities_municipalities(province_code: str, db: Annotated[Session, Depends(get_db)]) -> LocationsResponse:
    try:
        record = province.get(db, province_code)

        if record is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Province not found")

        rows = city.get_all(db, province_code=province_code)
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

@router.get("/{province_code}/barangays")
async def get_province_barangays(province_code: str, db: Annotated[Session, Depends(get_db)]) -> LocationsResponse:
    try:
        record = province.get(db, province_code)

        if record is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Province not found")

        rows = barangay.get_all(db, province_code=province_code)
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