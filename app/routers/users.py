from fastapi import APIRouter, HTTPException, Path
from sqlmodel import select, delete
from app.data.db import SessionDep
from app.models.user import User
from typing import Annotated, Any, Sequence

router = APIRouter(prefix="/users")

@router.get("/")
def get_all_users(session: SessionDep):
    """Restituisce tutti gli utenti presenti nel database"""
    users = session.exec(select(User)).all() 
    return users


    # Se è None
    database_user = User.model_validate(user_data) #controllo dati rispettino il modello
    
    session.add(database_user)
    session.commit()
    session.refresh(database_user)
    return "User added successfully"
    
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
    """Elimina tutti gli utenti dal database"""
    session.exec(delete(User))
    session.commit()
    return "All users successfully deleted"

@router.delete("/{username}")
def delete_single_user(username: str, session: SessionDep):
    """Elimina un singolo utente dal database"""
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return f"User {username} deleted!"