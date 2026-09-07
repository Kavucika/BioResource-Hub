from pydantic import BaseModel


class LocationRequest(BaseModel):
    address_line: str | None = None
    village: str | None = None
    city: str
    district: str | None = None
    state: str
    country: str = "India"
    pincode: str | None = None
    latitude: float | None = None
    longitude: float | None = None