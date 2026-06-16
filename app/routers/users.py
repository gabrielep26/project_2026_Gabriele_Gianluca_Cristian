from fastapi import APIRouter #crea gruppi di API (gruppo users)
from sqlmodel import select #query database
from app.data.db import SessionDep #connessione al database
from app.models.user import User #import tabella (classe) User da database

router = APIRouter(prefix="/users") #tutte api iniziano per /users

#get /users
@router.get("/") #quando arriva richiesta get /users esegui
def get_all_users(session: SessionDep): #azione su database
    """Restituisce tutti gli utenti presenti nel database"""
    users = session.exec(select(User)).all() 
    #query: select(User) prendi da tabella User all (tutti)
    return users #fastapi converte gli oggetti python in JSON e manda al frontend