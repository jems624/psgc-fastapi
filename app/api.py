from fastapi import FastAPI

from app.routers import (regions, provinces, cities, municipalities,
                        cities_municipalities, barangays)

app = FastAPI()

app.include_router(regions.router, prefix="/regions")
app.include_router(provinces.router, prefix="/provinces")
app.include_router(cities.router, prefix="/cities")
app.include_router(municipalities.router, prefix="/municipalities")
app.include_router(cities_municipalities.router, prefix="/cities-municipalities")
app.include_router(barangays.router, prefix="/barangays")