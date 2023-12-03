import logging

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.db.models import Location
from app.schemas.locations import LocationResponse, LocationsResponse
from app.crud import region, province, city, barangay
from app.constants import GeoLevels

router = APIRouter(tags=["Regions"])


@router.get("/")
async def get_regions(db: Annotated[Session, Depends(get_db)]) -> LocationsResponse:
    try:
        rows = region.get_all(db)
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

@router.get("/{region_code}")
async def get_region(region_code: str, db: Annotated[Session, Depends(get_db)]) -> LocationResponse:
    try:
        record = region.get(db, region_code)

        if record is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Region not found")

        return LocationResponse(
            code=record.code,
            name=record.name
        )

    except HTTPException as e:
        raise e

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/{region_code}/provinces")
async def get_region_provinces(region_code: str, db: Annotated[Session, Depends(get_db)]) -> LocationsResponse:
    try:
        record = region.get(db, region_code)

        if record is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Region not found")

        rows = province.get_all(db, region_code=region_code)
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

@router.get("/{region_code}/cities")
async def get_region_cities(region_code: str, db: Annotated[Session, Depends(get_db)]) -> LocationsResponse:
    try:
        record = region.get(db, region_code)

        if record is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Region not found")
        
        rows = city.get_all(db, region_code=region_code, geo_levels=[GeoLevels.City])
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

@router.get("/{region_code}/municipalities")
async def get_region_municipalities(region_code: str, db: Annotated[Session, Depends(get_db)]) -> LocationsResponse:
    try:
        record = region.get(db, region_code)

        if record is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Region not found")
        
        rows = city.get_all(db, region_code=region_code, geo_levels=[GeoLevels.Municipality])
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

@router.get("/{region_code}/cities-municipalities")
async def get_region_cities_municipalities(region_code: str, db: Annotated[Session, Depends(get_db)]) -> LocationsResponse:
    try:
        record = region.get(db, region_code)

        if record is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Region not found")
        
        rows = city.get_all(db, region_code=region_code)
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

@router.get("/{region_code}/barangays")
async def get_region_barangays(region_code: str, db: Annotated[Session, Depends(get_db)]) -> LocationsResponse:
    try:
        record = region.get(db, region_code)

        if record is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Region not found")
        
        rows = barangay.get_all(db, region_code=region_code)
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