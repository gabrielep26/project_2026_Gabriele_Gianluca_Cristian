from fastapi import APIRouter
from sqlmodel import select, delete
from app.data.db import SessionDep
from app.models.event import Event, EventCreate

router = APIRouter(prefix="/events")

@router.get("/")
def get_all_events(session: SessionDep):
    """Endpoint to obtain all events"""
    events = session.exec(select(Event)).all()
    return events

@router.post("/")
def add_event(session: SessionDep, event: EventCreate):
    """Endpoint to add a new event"""
    
    database_event = Event.model_validate(event)
    session.add(database_event)
    session.commit()
    
    session.refresh(database_event)
    
    return "Event successfully added"

@router.delete("/")
def delete_all(session: SessionDep):
    """Endpoint to delete all the events"""
    session.exec(delete(Event))
    session.commit()
    return "All events successfully deleted"