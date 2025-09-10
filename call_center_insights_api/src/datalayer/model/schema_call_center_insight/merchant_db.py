from datetime import datetime
from sqlmodel import Field, SQLModel


class MerchantDB(SQLModel, table=True):
    __tablename__ = "merchant"
    __table_args__ = {"schema": "public"}

    merchant_id: int = Field(primary_key=True)
    merchant_name: str = Field(nullable=False)
    merchant_brand: str = Field(nullable=True)
    merchant_status: str = Field(nullable=True)
    merchant_city: str = Field(nullable=True)
    merchant_district: str = Field(nullable=True)
    merchant_address: str = Field(nullable=True)
    merchant_tax_no: str = Field(nullable=True)
    merchant_tax_office: str = Field(nullable=True)
    merchant_sector: str = Field(nullable=True)
    merchant_people: int = Field(nullable=True)
    merchant_hardware: str = Field(nullable=True)
    merchant_fiscal_no: str = Field(nullable=True)
    merchant_service: str = Field(nullable=True)
    merchant_ticket: str = Field(nullable=True)
    merchant_inserted_at: datetime = Field(nullable=False)