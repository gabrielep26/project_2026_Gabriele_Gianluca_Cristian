from datetime import datetime
from sqlmodel import SQLModel, Field


class Event(SQLModel, table=True):
    title: str
    description: str
    date: datetime
    location: str
    id: int = Field(default=None,primary_key=True)
