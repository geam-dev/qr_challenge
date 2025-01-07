from datetime import datetime 

from fastapi import APIRouter, HTTPException, status, Request, Depends, Query 
from fastapi.responses import Response, RedirectResponse

from sqlalchemy.orm import Session 

from src.services.qr_codes import get_qr_code_img_bytes
from src.services.client_info import get_client_country_from_ip, validate_ip
from src.services import crud, auth
from src import schemas, models, db

from uuid import UUID

import os



router = APIRouter()

# Create QRCode
@router.post(
    "/qrcode", 
    tags=["QRCodes"],
    summary="Create QR Code"
)
def post_qrcode(
    qr_code: schemas.QrCodeCreate,
    user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(db.get_db)
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
@router.put(
    "/qrcode", 
    tags=["QRCodes"],
    summary="Update QR Code metadata",
)
def update_qr_codes(
    qr_code: schemas.QrCodeUpdate,
    user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(db.get_db)
):
    # Get QRCode
    db_qr = crud.update_qr_code(db=db, qr_code=qr_code, user_uuid=user.uuid)

    # If not found
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
@router.get(
    "/qrcode", 
    tags=["QRCodes"],
    summary="Get QR Code Image based on UUID"
)
def get_qr_code(
    qr_uuid: UUID = Query(...),
    user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(db.get_db),
):
    # Get QRCode based on qr_uuid and user_uuid
    db_qr = crud.get_qr_code(db=db, qr_uuid=qr_uuid, user_uuid=user.uuid)

    # If not found
    if not db_qr:
        raise HTTPException(
            status_code=404,
            detail="QR Code with that uuid not found for logged user."
        )
    
    # Build Image
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
@router.get(
    "/qrcodes", 
    tags=["QRCodes"],
    summary="List all user QR Codes"
)
def get_qr_codes(
    limit: int = 10,
    page: int = 1,
    user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(db.get_db),
):
    return crud.get_user_qr_codes(db=db, user_uuid=user.uuid, limit=limit, offset=limit * (page-1))

# Scan QRCode
@router.get(
    "/scan", 
    tags=["QRCodes"],
    summary="Scan QR Code (Not works in Swagger for technical reasons, try in browser)"
)
def scan_qr_code(
    request: Request,
    qr_uuid: UUID = Query(...),
    db: Session = Depends(db.get_db)
):
    # Get Client IP
    client_ip = request.client.host if request.client else None 
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(',')[0].strip()
    
    # Validate Client IP
    if not validate_ip(client_ip):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Client IP not valid",
        )

    # Create scan in DB
    db_scan = crud.create_scan(
        db=db,
        qr_uuid=qr_uuid,
        client_ip=client_ip,
        country=get_client_country_from_ip(
            client_ip,
            os.getenv('IP_INFO_ACCESS_TOKEN')
        ),
    )
    
    # Get QRCode
    db_qr = crud.get_qr_code(db=db, qr_uuid=qr_uuid)

    if not db_qr:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="QR Code Not Found",
        )

    return RedirectResponse(
        url=db_qr.url,
        status_code=status.HTTP_302_FOUND
    )


# Analytics
@router.get(
    "/analytics", 
    tags=["QRCodes"],
    summary="Get Analytics from our QR Codes"
)
def get_analytics(
    user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(db.get_db),
):
    return crud.get_qr_code_analytics(db=db, user_uuid=user.uuid)