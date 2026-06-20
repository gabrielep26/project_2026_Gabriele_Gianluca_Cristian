from sqlmodel import SQLModel,Field

# 1. Base fields shared by everyone
class UserBase(SQLModel):
    username: str
    name: str
    email: str


# 2. What the client sends in the POST request
class UserCreate(UserBase):
    pass


# 3. What is saved in the database
class User(UserBase, table=True):
    username: str = Field(primary_key=True)
    pass