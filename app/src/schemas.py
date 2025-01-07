from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID


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
    email: EmailStr
    password: str 


class QrCodeCreate(BaseModel):
    url: str
    color: str 
    size: str 


class QrCodeUpdate(QrCodeCreate):
    uuid: UUID


class ScanCreate(BaseModel):
    qr_uuid: UUID 
    ip: str 
    country: str

