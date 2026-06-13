from fastapi import APIRouter
from sqlmodel import select
from app.data.db import SessionDep
from app.models.event import Event

router = APIRouter(prefix="/events")

@router.get("/")
def get_all_events(session: SessionDep):
    """Endpoint to obtain all events"""
    events = session.exec(select(Event)).all()
    return events

@router.post("/")
def add_event(session: SessionDep, event: Event):
    """Endpoint to add a new event"""
    session.add(Event.model_validate(event))
    session.commit()
    return "Event successfully added"