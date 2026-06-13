from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    username: str = Field(primary_key=True)
    name: str
    #unique parameter makes email a unique constraint alongside the primary key
    email: str = Field(unique=True)



