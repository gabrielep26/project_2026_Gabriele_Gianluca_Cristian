from fastapi import APIRouter
from sqlmodel import select #query database
from app.data.db import SessionDep #connessione al database
from app.models.user import Registration #import tabella (classe) Registration da database

router = APIRouter(prefix="/registrations") #tutte api iniziano per /registrations

@router.get("/") 
def get_all_registrations(session: SessionDep):
    """Restituisce tutte le registrazioni presenti nel database"""
    registrations = session.exec(select(Registration)).all() 
    return registrations


