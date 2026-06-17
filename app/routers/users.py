from fastapi import APIRouter
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

@router.post("/")
def add_user(user: User, session: SessionDep):
    """Aggiunge un nuovo utente al database"""
 
    # Controlliamo se esiste già un utente con lo stesso username
    existing_user = session.get(User, user.username) #ricerca con chiave primaria
    
    if existing_user: #è true
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username already existing"
        )

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


