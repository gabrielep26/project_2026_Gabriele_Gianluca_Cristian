from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    username: str = Field(primary_key=True)
    name: str
    #unique indica che deve essere univoco(aparte dalla primary key)
    email: str = Field(unique=True)



