# schemas.py

from pydantic import BaseModel

class ApplicationResponse(BaseModel):
    id: int
    fullName: str
    phone: str
    email: str
    resumePath: str
    photoPath: str
    address: str
    position: str
    gender: str
    qualification: str
    reference: str
