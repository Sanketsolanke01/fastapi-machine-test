from pydantic import BaseModel
from typing import List


class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class ProjectOut(BaseModel):
    id: int
    project_name: str

    class Config:
        from_attributes = True



class ClientCreate(BaseModel):
    client_name: str


class ClientDetail(BaseModel):
    id: int
    client_name: str
    created_by: str
    projects: List[ProjectOut] = []

    class Config:
        from_attributes = True



class ProjectCreate(BaseModel):
    project_name: str
    client_id: int
    users: List[int]