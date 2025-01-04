from sqlalchemy.orm import Session 
from sqlalchemy import func 
from models import User, QrCode, Scan
from schemas import (
    UserCreate, 
    QrCodeCreate,
    QrCodeUpdate,
    ScanCreate
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
    return db.query(QrCode).filter(
        QrCode.uuid == qr_code.uuid,
        QrCode.user_uuid == user_uuid,
    ).first()


def get_qr_code(
    db: Session,
    qr_uuid: str,
):
    return db.query(QrCode).filter(
        QrCode.uuid==qr_uuid
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
    timezone: str,
):
    db_scan = Scan(
        qr_uuid=qr_uuid,
        ip=client_ip,
        country=country,
        timezone=timezone,
    )
    db.add(db_scan)
    db.commit()
    db.refresh(db_scan)
    return db_scan