from fastapi import APIRouter, HTTPException, Path
from sqlmodel import select, delete
from app.data.db import SessionDep
from app.models.event import Event, EventCreate
from typing import Annotated

router = APIRouter(prefix="/events")

@router.get("/")
def get_all_events(session: SessionDep):
    """Endpoint to obtain all events"""
    events = session.exec(select(Event)).all()
    return events

@router.get("/{id}")
def get_event(session : SessionDep, id: Annotated[int, Path(description="event id to obtain")]):
    session = session.get(Event, id)
    if not session:
        raise HTTPException(status_code=404, detail="Event not found")
    return session

@router.put("/{id}")
def update(session : SessionDep, event: EventCreate):
    events = session.exec(select(Event)).all()
    if event.id not in events:
        raise HTTPException(404, detail="No event found!")
    events[event.id] = event
    
    
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

@router.delete("/{id}")
def delete_single(session: SessionDep, id: Annotated[int, Path(description="Id that should be deleted")]):
    event = session.get(Event, id)
    if not event:
        raise HTTPException(404, detail="Event non trovato")
    session.delete(Event[id])
    session.commit()
    return f"Event {id} deleted!"
@router.post("/")
def add_event(session: SessionDep, event: Event):
    """Endpoint to add a new event"""
    session.add(Event.model_validate(event))
    session.commit()
    return "Event successfully added"