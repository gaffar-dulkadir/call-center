from datetime import datetime
from sqlmodel import Field, SQLModel


class MerchantContactDB(SQLModel, table=True):
    __tablename__ = "merchant_contact"
    __table_args__ = {"schema": "public"}

    contact_id: int = Field(primary_key=True)
    merchant_id: int = Field(foreign_key="call_center_insight.merchant.merchant_id", nullable=False)