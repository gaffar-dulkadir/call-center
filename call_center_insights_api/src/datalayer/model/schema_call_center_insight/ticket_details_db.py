from datetime import datetime
from sqlmodel import Field, SQLModel


class TicketDetailsDB(SQLModel, table=True):
    __tablename__ = "ticket_details"
    __table_args__ = {"schema": "public"}

    ticket_id: int = Field(primary_key=True, foreign_key="call_center_insight.merchant_ticket.merchant_ticket_id")
    ticket_detail: str = Field(nullable=True)