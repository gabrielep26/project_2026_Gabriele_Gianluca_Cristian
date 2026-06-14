from fastapi import APIRouter
from sqlmodel import select
from app.data.db import SessionDep
from app.models.user import User

router = APIRouter(prefix="/users")

@router.get("/")
def get_all_users(session: SessionDep):
    """Returns the list of all users"""
    users = session.exec(select(User)).all()
    return users

