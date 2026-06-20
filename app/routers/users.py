from fastapi import APIRouter, HTTPException, Path
from sqlmodel import select, delete
from app.data.db import SessionDep
from app.models.user import User,UserCreate
from app.models.registration import Registration
from typing import Annotated, Any, Sequence

router = APIRouter(prefix="/users")

@router.get("/")
def get_all_users(session: SessionDep):
    """Restituisce tutti gli utenti presenti nel database"""
    users = session.exec(select(User)).all() 
    return users

@router.post("/")
def add_user(user: UserCreate, session: SessionDep):
    """Aggiunge un nuovo utente al database"""

    # Controlliamo se esiste già un utente con lo stesso username
    existing_user = session.get(User, user.username)  # ricerca con chiave primaria

    if existing_user:  # è true
        raise HTTPException(
            status_code=400,
            detail="Username already existing"
        )

    # Se è None
    database_user = User.model_validate(user)  # controllo dati rispettino il modello

    session.add(database_user)
    session.commit()
    session.refresh(database_user)
    return database_user

@router.get("/{username}")
def get_user(username: str, session: SessionDep):
    """Restituisce l'utente con lo username indicato"""
    session = session.exec(select(User).where(User.username == username)).first()
    if not session:
        raise HTTPException(status_code=404, detail="User not found")
    #query: select(User) prendi da tabella User where username == username
    return session

@router.delete("/")
def delete_all_users(session: SessionDep):
    """Elimina tutti gli utenti dal database e le loro registrazioni"""
    #Deletes registrations
    session.exec(delete(Registration))
    session.exec(delete(User))
    session.commit()
    return "All users successfully deleted"

@router.delete("/{username}")
def delete_single_user(username: str, session: SessionDep):
    """Elimina un singolo utente dal database e le sue registrazioni"""
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    #Deletes user registrations in cascade
    registrations = session.exec(
        select(Registration).where(Registration.username==username)
    ).all()

    for reg in registrations:
        session.delete(reg)

    session.delete(user)
    session.commit()
    return f"User {username} deleted!"
