from fastapi import APIRouter, HTTPException, Path
from sqlmodel import select, delete
from app.data.db import SessionDep
from app.models.event import Event, EventCreate
from app.models.user import User, UserCreate
from app.models.registration import Registration
from app.routers.users import add_user
from typing import Annotated

router = APIRouter(prefix="/events")

@router.get("/")
def get_all_events(session: SessionDep):
    """Endpoint to obtain all events"""
    events = session.exec(select(Event)).all()
    return events

@router.get("/{id}")
def get_event(session : SessionDep, id: Annotated[int, Path(description="event id to obtain")]):
    """Endpoint to get an existing single event"""
    session = session.get(Event, id)
    if not session:
        raise HTTPException(status_code=404, detail="Event not found")
    return session

@router.put("/{id}", response_model=Event)
def update(session: SessionDep, id: int, event_data: EventCreate):
    """Endpoint to change an existing single event"""
    
    db_event = session.get(Event, id)
    if not db_event:
        raise HTTPException(status_code=404, detail="No event found!")
    
    update_dict = event_data.model_dump(exclude_unset=True)
    
    for key, value in update_dict.items():
        setattr(db_event, key, value)
    
    session.add(db_event)
    session.commit()
    
    session.refresh(db_event)
    
    return db_event
    
    
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
             user:UserCreate):
    """Endpoint to register to an event, if the user doesn't exist it's created automatically"""
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    user_in_db = session.get(User, user.username)

    if not user_in_db:
        user_in_db =add_user(user,session)

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
    session.exec(delete(Registration))
    session.flush()
    session.exec(delete(Event))
    session.commit()
    return "All events successfully deleted"

@router.delete("/{id}")
def delete_single(session: SessionDep, id: Annotated[int, Path(description="Id that should be deleted")]):
    """Endpoint to delete a single event"""
    event = session.get(Event, id)
    if not event:
        raise HTTPException(404, detail="Event non trovato")
    
    command = delete(Registration).where(Registration.event_id == id)
    session.exec(command)
    session.flush()  
    session.delete(event)
    session.commit()
    return f"Event {id} deleted!"

