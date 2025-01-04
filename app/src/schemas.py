from pydantic import BaseModel
from typing import Optional


# Auth
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserCreate(BaseModel):
    email: str
    password: str
#

class UserCreate(BaseModel):
    email: str 
    password: str 


class QrCodeCreate(BaseModel):
    url: str
    color: str 
    size: str 


class QrCodeUpdate(QrCodeCreate):
    uuid: str


class ScanCreate(BaseModel):
    qr_uuid: str 
    ip: str 
    country: str

