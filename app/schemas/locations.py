from pydantic import BaseModel

class LocationResponse(BaseModel):
    code: str
    name: str

class LocationsResponse(BaseModel):
    regions: list[LocationResponse]