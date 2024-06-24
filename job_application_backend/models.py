from pydantic import BaseModel
 
class Application(BaseModel):
    fullName: str
    phone: str
    email: str
    address: str
    position: str
    gender: str
    qualification: str
    reference: str