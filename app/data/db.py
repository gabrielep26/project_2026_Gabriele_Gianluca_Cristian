from sqlmodel import create_engine, SQLModel, Session, select
from typing import Annotated
from fastapi import Depends
import os
from faker import Faker
from app.config import config
import random

from app.models.registration import Registration  # NOQA
from app.models.event import Event
from app.models.user import User

sqlite_file_name = config.root_dir / "data/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args, echo=True)


def init_database() -> None:
    ds_exists = os.path.isfile(sqlite_file_name)
    SQLModel.metadata.create_all(engine)
    if not ds_exists:
        f = Faker("it_IT")
        with Session(engine) as session:

            for i in range (10):
                event = Event(title=f.sentence(nb_words=10), description=f.sentence(nb_words=20),date=f.date_time_this_year(), location=f.sentence(nb_words=10))
                session.add(event)
            session.commit()

            for i in range(10):
                user = User(username=f.user_name(),name=f.name(),email=f.email())
                session.add(user)
            session.commit()

            #Now we are linking the events and users

            #Selects all the users and events created with faker
            users = session.exec(select(User)).all()
            events = session.exec(select(Event)).all()

            #set() keeps track of unique user-event tuples of their primary keys
            u_e_tuples = set()

            #Creates 10 registrations
            while len(u_e_tuples) < 10:
                random_user=random.choice(users)
                random_event=random.choice(events)

                #Creates a tuple of user-event
                u_e_tuple=(random_user.username,random_event.id)

                if u_e_tuple not in u_e_tuples:
                    u_e_tuples.add(u_e_tuple)

                    #Creates the registration of the tuple
                    registration = Registration(username=random_user.username,event_id=random_event.id)
                    session.add(registration)

            session.commit()

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

#chad