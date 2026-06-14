from fastapi import APIRouter, HTTPException, Path
from sqlmodel import select, delete
from app.data.db import SessionDep
from app.models.event import Event, EventCreate
from app.models.user import User
from app.models.registration import Registration
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

@router.post("/{id}/register")
def register(session: SessionDep,
             id: Annotated[int, Path(description="Id of the event for registration")],
             user:User):
    """Endpoint to register to an event, if the user doesn't exist it's created automatically"""
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    #This has to be replaced with the endpoint post/users  ->
    user_in_db = session.get(User,user.username)

    if not user_in_db:
        user_in_db = user
        session.add(user_in_db)
        session.commit()
        session.refresh(user_in_db)
    #<-Until here

    """We have to verify if the user is already registered"""
    user_registered = session.exec(
        select(Registration).where(
            Registration.username == user_in_db.username,
            Registration.event_id == event.id
        )
    ).first()
    if not user_registered:
        new_registration = Registration(username=user_in_db.username, event_id=event.id)
        session.add(new_registration)
        session.commit()

    return {"message": f"User {user_in_db.username} registered to the event"}


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