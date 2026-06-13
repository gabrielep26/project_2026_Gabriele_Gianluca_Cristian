from fastapi import APIRouter
from sqlmodel import select
from app.data.db import SessionDep
from app.models.event import Event

router = APIRouter(prefix="/events")

@router.get("/")
def get_all_events(session: SessionDep):
    events = session.exec(select(Event)).all()
    return events