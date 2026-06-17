from fastapi import APIRouter
from sqlmodel import select #query database
from app.data.db import SessionDep #connessione al database
from app.models.registration import Registration #import tabella (classe) Registration da database

router = APIRouter(prefix="/registrations") #tutte api iniziano per /registrations

@router.get("/") 
def get_all_registrations(session: SessionDep):
    """Restituisce tutte le registrazioni presenti nel database"""
    registrations = session.exec(select(Registration)).all() 
    return registrations

@router.delete("/")
def delete_registration(username: str, event_id: int, session: SessionDep):
    """
    Endpoint per eliminare una singola registrazione tramite query parameters.
    Lancia un errore 404 se la registrazione non esiste.
    """
    # Cerchiamo la registrazione nel database
    registration = session.get(Registration, (username, event_id))
    
    # Se None
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    
    # Se esiste la eliminiamo
    session.delete(registration)
    session.commit()
    
    return f"Registration for user '{username}' in event {event_id} successfully deleted"