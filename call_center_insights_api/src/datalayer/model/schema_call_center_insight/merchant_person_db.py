from datetime import datetime
from sqlmodel import Field, SQLModel


class MerchantPersonDB(SQLModel, table=True):
    __tablename__ = "merchant_person"
    __table_args__ = {"schema": "public"}

    merchant_id: int = Field(primary_key=True, foreign_key="call_center_insight.merchant.merchant_id")
    merchant_person_state: int = Field(nullable=True)  # Fixed: database stores as integer
    merchant_person_name: str = Field(nullable=True)
    merchant_person_phone: str = Field(nullable=True)