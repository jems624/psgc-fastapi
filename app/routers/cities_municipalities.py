import logging

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.db.models import Location
from app.schemas.locations import LocationResponse, LocationsResponse
from app.crud import city, barangay

router = APIRouter(tags=["Cities / Municipalities"])


@router.get("/")
async def get_cities_municipalities(db: Annotated[Session, Depends(get_db)]) -> LocationsResponse:
    try:
        rows = city.get_all(db)
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

@router.get("/{city_municipality_code}")
async def get_city_municipality(city_municipality_code: str, db: Annotated[Session, Depends(get_db)]) -> LocationResponse:
    try:
        record = city.get(db, city_municipality_code)

        if record is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City / Municipality not found")

        return LocationResponse(
            code=record.code,
            name=record.name
        )

    except HTTPException as e:
        raise e

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/{city_municipality_code}/barangays")
async def get_city_barangays(city_municipality_code: str, db: Annotated[Session, Depends(get_db)]) -> LocationsResponse:
    try:
        rows = barangay.get_all(db, city_code=city_municipality_code)

        record = city.get(db, city_municipality_code)

        if record is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City / Municipality not found")

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