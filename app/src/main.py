from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException, status, Request, Query, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import Response, RedirectResponse

from datetime import timedelta 

from sqlalchemy.orm import Session

import crud, auth, schemas, dependencies
from models import User
from tempfile import NamedTemporaryFile
from services import get_qr_code_img_bytes

import os, qrcode, io, requests

app = FastAPI()


# Get Token
@app.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(dependencies.get_db),
):
    user = auth.authenticate_user(db=db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token_expires = timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
    access_token = auth.create_access_token(
        data={"sub": user.email}, 
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# Register User
@app.post("/register")
def register(
    user: schemas.UserCreate,
    db: Session = Depends(dependencies.get_db)
):
    db_user = crud.create_user(db=db, email=user.email, password_hash=auth.get_password_hash(user.password))
    return {"email": db_user.email}

# Create QRCode
@app.post("/qrcode")
async def post_qrcode(
    qr_code: schemas.QrCodeCreate,
    user: User = Depends(auth.get_current_user),
    db: Session = Depends(dependencies.get_db)
):
    db_qr = crud.create_qr_code(db=db, qr_code=qr_code, user_uuid=user.uuid)
    
    qr_code_image_bytes = get_qr_code_img_bytes(
        data=f"{os.getenv('APP_URL')}/scan?qr_uuid={db_qr.uuid}",
        size=qr_code.size,
        color=qr_code.color,
    )

    return Response(
        content=qr_code_image_bytes,
        media_type="image/png"
    )


# Update QRCode
@app.put("/qrcode")
async def update_qr_codes(
    qr_code: schemas.QrCodeUpdate,
    user: User = Depends(auth.get_current_user),
    db: Session = Depends(dependencies.get_db)
):
    db_qr = crud.update_qr_code(db=db, qr_code=qr_code, user_uuid=user.uuid)

    if not db_qr:
        raise HTTPException(
            status_code=404,
            detail="QR Code with that uuid not found for logged user."
        )

    qr_code_image_bytes = get_qr_code_img_bytes(
        data=f"{os.getenv('APP_URL')}/scan?qr_uuid={db_qr.uuid}",
        size=qr_code.size,
        color=qr_code.color
    )

    return Response(
        content=qr_code_image_bytes,
        media_type="image/png"
    )


# Get QRCode
@app.get("/qrcode")
async def get_qr_code(
    qr_uuid: str,
    user: User = Depends(auth.get_current_user),
    db: Session = Depends(dependencies.get_db),
):
    db_qr = crud.get_qr_code(db=db, qr_uuid=qr_uuid)

    if db_qr.user_uuid != user.uuid:
        return HTTPException(
            status_code=404,
            detail="QR Code with that uuid not found for logged user."
        )
    
    qr_code_image_bytes = get_qr_code_img_bytes(
        data=f"{os.getenv('APP_URL')}/scan?qr_uuid={db_qr.uuid}",
        size=db_qr.size,
        color=db_qr.color
    )

    return Response(
        content=qr_code_image_bytes,
        media_type="image/png"
    )


# List QRCodes
@app.get("/qrcodes")
async def get_qr_codes(
    limit: int = 10,
    page: int = 1,
    user: User = Depends(auth.get_current_user),
    db: Session = Depends(dependencies.get_db),
):
    return crud.get_user_qr_codes(db=db, user_uuid=user.uuid, limit=limit, offset=limit * (page-1))

# Scan QRCode
@app.get("/scan")
async def scan_qr_code(
    request: Request,
    qr_uuid: str = Query(...),
    db: Session = Depends(dependencies.get_db)
):
    db_qr = get_qr_code(db=db, qr_uuid=qr_uuid)

    # TODO: Capture request data

    if not db_qr:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="QR Code Not Found",
        )

    return RedirectResponse(
        url=db_qr.url,
        status_code=status.HTTP_302_FOUND
    )