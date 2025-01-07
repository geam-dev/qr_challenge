from sqlalchemy.orm import Session 
from sqlalchemy import func 
from src.models import User, QrCode, Scan
from src.schemas import (
    QrCodeCreate,
    QrCodeUpdate,
)

# Users
def create_user(
    db: Session,
    email: str,
    password_hash: str,
):
    db_user = User(
        email=email,
        password_hash=password_hash
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(
    db: Session, 
    email: str,
) -> User:
    return db.query(User).filter(
        User.email == email
    ).first()


# QrCodes 
def create_qr_code(
    db: Session,
    qr_code: QrCodeCreate,
    user_uuid: str,
):
    db_qr_code = QrCode(
        url=qr_code.url,
        color=qr_code.color,
        size=qr_code.size,
        user_uuid=user_uuid
    )
    db.add(db_qr_code)
    db.commit()
    db.refresh(db_qr_code)
    return db_qr_code


def update_qr_code(
    db: Session,
    qr_code: QrCodeUpdate,
    user_uuid: str,
):
    db_qr_code = db.query(QrCode).filter(
        QrCode.uuid == qr_code.uuid,
        QrCode.user_uuid == user_uuid,
    ).first()

    if not db_qr_code:
        return None 
    
    if qr_code.url:
        db_qr_code.url = qr_code.url 
    if qr_code.color:
        db_qr_code.color = qr_code.color
    if qr_code.size:
        db_qr_code.size = qr_code.size
    
    db_qr_code.updated_at = func.now()

    db.commit()
    db.refresh(db_qr_code)
    return db_qr_code


def get_qr_code(
    db: Session,
    qr_uuid: str,
    user_uuid: str,
):
    return db.query(QrCode).filter(
        QrCode.uuid == qr_uuid,
        QrCode.user_uuid == user_uuid,
    ).first()

def get_user_qr_codes(
    db: Session,
    user_uuid: str,
    limit: int,
    offset: int,
):
    return db.query(QrCode).filter(
        QrCode.user_uuid==user_uuid
    ).offset(offset).limit(limit).all()


# Scans
def create_scan(
    db: Session,
    qr_uuid: str,
    client_ip: str,
    country: str,
):
    db_scan = Scan(
        qr_uuid=qr_uuid,
        ip=client_ip,
        country=country,
    )
    db.add(db_scan)
    db.commit()
    db.refresh(db_scan)
    return db_scan


# Stats
def get_qr_code_analytics(
    db: Session,
    user_uuid: str,
):
    # Get all user QRCodes
    db_qr_codes = db.query(QrCode).filter(
        QrCode.user_uuid == user_uuid
    ).all()

    result = []

    for db_qr_code in db_qr_codes:
        # Get QRCode scans
        scans = db.query(Scan).filter(
            Scan.qr_uuid == db_qr_code.uuid
        ).all()

        # Parse QRCode data and scans data
        qr_code_info = {
            "uuid": db_qr_code.uuid,
            "url": db_qr_code.url,
            "color": db_qr_code.color,
            "size": db_qr_code.size,
            "scans_count": len(scans),
            "scans": [
                {
                    "uuid": scan.uuid,
                    "ip": scan.ip,
                    "country": scan.country,
                    "created_at": scan.created_at,
                } for scan in scans
            ]
        }

        # Add to result
        result.append(qr_code_info)
    
    return result