import uuid
from datetime import datetime
from typing import Literal

from sqlalchemy import TIMESTAMP, Index, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

Status = Literal["created", "queued", "success", "failed"]


class Base(DeclarativeBase):
    """Base declarative class for all models."""

    pass


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, nullable=False, server_default=text("gen_random_uuid()")
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=text("now()"),
        onupdate=text("now()"),
    )


class Address(BaseModel):
    __tablename__ = "addresses"
    __table_args__ = (Index("ix_addresses_status", "status"),)

    brightdata_response_id: Mapped[str] = mapped_column(
        comment="Job response ID from BrightData."
    )
    input_address: Mapped[str] = mapped_column(
        nullable=False, comment="The input address to be looked up."
    )
    streeteasy_url: Mapped[str | None] = mapped_column(
        comment="URL of the StreetEasy listing for the matched address/unit."
    )
    streeteasy_unit_name: Mapped[str | None] = mapped_column(
        comment="Unit name from the matched StreetEasy listing."
    )
    streeteasy_unit_address: Mapped[str | None] = mapped_column(
        comment="Full address of the unit from the matched StreetEasy listing."
    )
    has_active_listing: Mapped[bool] = mapped_column(
        comment="Whether StreetEasy has an active listing for the provided address."
    )
    is_address_match: Mapped[bool] = mapped_column(
        comment="Whether the address returned by StreetEasy matches the input address."
    )
    status: Mapped[Status] = mapped_column(
        nullable=False,
        comment="The current processing status of the address lookup job.",
    )
