from datetime import datetime
from sqlmodel import SQLModel, Field

# 1. Base fields shared by everyone
class EventBase(SQLModel):
    title: str
    description: str
    date: str  # or datetime
    location: str


# 2. What the client sends in the POST request (NO "id" field here!)
class EventCreate(EventBase):
    pass


# 3. What is saved in the database (with "id")
class Event(EventBase, table=True):
    id: int | None = Field(default=None, primary_key=True)