from datetime import datetime
from sqlalchemy import (
    BigInteger,
    DateTime,
    UUID,
    ForeignKey,
    Integer,
    MetaData,
    String,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column 
import uuid as uuid_lib

metadata = MetaData()
metadata.schema = "qr_challenge"

class Base(DeclarativeBase):
    metadata = metadata 

class User(Base):
    __tablename__ = 'users'

    uuid: Mapped[uuid_lib.UUID] = mapped_column(
        UUID(as_uuid=True),
        default=lambda: uuid_lib.uuid4(),
        primary_key=True
    )
    email: Mapped[str] = mapped_column(String)
    password_hash: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )

class QrCode(Base):
    __tablename__ = 'qr_codes'

    uuid: Mapped[uuid_lib.UUID] = mapped_column(
        UUID(as_uuid=True),
        default=lambda: uuid_lib.uuid4(),
        primary_key=True
    )
    url: Mapped[str] = mapped_column(String)
    color: Mapped[str] = mapped_column(String)
    size: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    user_uuid: Mapped[uuid_lib.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(User.uuid),
        index=True,
    )

class Scan(Base):
    __tablename__ = 'scans'

    uuid: Mapped[uuid_lib.UUID] = mapped_column(
        UUID(as_uuid=True),
        default=lambda: uuid_lib.uuid4(),
        primary_key=True
    )
    qr_uuid: Mapped[uuid_lib.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(QrCode.uuid),
        index=True,
    )
    ip: Mapped[str] = mapped_column(String)
    country: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )