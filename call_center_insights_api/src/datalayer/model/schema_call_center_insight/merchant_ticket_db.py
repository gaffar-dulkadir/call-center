from datetime import datetime
from sqlmodel import Field, SQLModel


class MerchantTicketDB(SQLModel, table=True):
    __tablename__ = "merchant_ticket"
    __table_args__ = {"schema": "public"}

    merchant_ticket_id: int = Field(primary_key=True, sa_column_kwargs={"name": "mercant_ticket_id"})  # Fixed: actual DB column name
    merchant_id: int = Field(foreign_key="call_center_insight.merchant.merchant_id", nullable=False)
    merchant_ticket_order_no: int = Field(nullable=True)
    merchant_ticket_type_id: int = Field(nullable=True)
    merchant_ticket_time: datetime = Field(nullable=True)
    merchant_ticket_kind_id: int = Field(nullable=True)
    merchant_ticket_sub_type_id: int = Field(nullable=True)
    merchant_ticket_explanation: str = Field(nullable=True)
    merchant_ticket_first_explanation: str = Field(nullable=True)