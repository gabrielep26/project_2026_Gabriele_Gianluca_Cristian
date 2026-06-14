from fastapi import APIRouter, HTTPException, Path
from sqlmodel import select, delete
from app.data.db import SessionDep
from app.models.user import User
from typing import Annotated, Any, Sequence

router = APIRouter(prefix="/users")

@router.get("/")
def get_all_users(session: SessionDep):
    """Returns the list of all users"""
    users = session.exec(select(User)).all()
    return users

