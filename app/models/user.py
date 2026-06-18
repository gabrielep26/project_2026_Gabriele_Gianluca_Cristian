from sqlmodel import SQLModel, Field

class UserBase(SQLModel, table=True):
    username: str = Field(primary_key=True)
    name: str
    email: str

class UserCreate(UserBase):
    pass

# 3. What is saved in the database (with "id")
class User(UserBase,  table=True):
    id: int | None = Field(default=None, primary_key=True)