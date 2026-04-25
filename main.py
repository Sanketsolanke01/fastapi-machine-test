from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import Base, engine
from models import User, Client, Project
from schemas import *
from deps import get_db, get_current_user
from auth import hash_password, verify_password, create_token

Base.metadata.create_all(bind=engine)

app = FastAPI()



@app.post("/users/")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    return {"msg": "User created"}


@app.post("/auth/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_token({"id": db_user.id})
    return {"access_token": token}


@app.get("/users/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()




@app.post("/clients/")
def create_client(client: ClientCreate, db: Session = Depends(get_db), token: str = Header(...)):
    user = get_current_user(token, db)

    db_client = Client(
        client_name=client.client_name,
        created_by=user.name
    )

    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


@app.get("/clients/")
def list_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()


@app.get("/clients/{id}", response_model=ClientDetail)
def client_detail(id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == id).first()

    if not client:
        raise HTTPException(status_code=404, detail="Not found")

    return client


@app.delete("/clients/{id}")
def delete_client(id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == id).first()

    if not client:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(client)
    db.commit()
    return {"msg": "Deleted"}


@app.put("/clients/{id}")
def update_client(id: int, data: ClientCreate, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == id).first()

    if not client:
        raise HTTPException(404, "Not found")

    client.client_name = data.client_name
    db.commit()
    db.refresh(client)

    return client




@app.post("/projects/")
def create_project(project: ProjectCreate, db: Session = Depends(get_db), token: str = Header(...)):
    user = get_current_user(token, db)

    users = db.query(User).filter(User.id.in_(project.users)).all()

    if len(users) != len(project.users):
        raise HTTPException(status_code=400, detail="Invalid users")

    db_project = Project(
        project_name=project.project_name,
        client_id=project.client_id,
        users=users
    )

    db.add(db_project)
    db.commit()
    return {"msg": "Project created"}


@app.get("/projects/")
def my_projects(db: Session = Depends(get_db), token: str = Header(...)):
    user = get_current_user(token, db)

    return [
        {
            "id": p.id,
            "project_name": p.project_name,
            "client_name": p.client.client_name
        }
        for p in user.projects
    ]


@app.delete("/projects/{id}")
def delete_project(id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(project)
    db.commit()
    return {"msg": "Deleted"}