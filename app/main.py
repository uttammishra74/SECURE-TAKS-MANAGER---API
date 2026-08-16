from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import delete
from sqlalchemy.orm import Session

import app.Model.models
from app.Authentication.auth import create_token, oauth2_scheme, verify_token
from app.Database.database import SessionLocal, engine
from app.Model.models import Task, User
from app.Schemas.schemas import TaskCreate, TaskResponse, UserCreate, UserResponse

app.Model.models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Secure Task Manager API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Welcome to Database"}


@app.post("/Register", response_model=UserResponse)
def Users(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=user.password,
    )
    email_exists = db.query(User).filter(User.email == new_user.email).first()
    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered",
        )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or user.password_hash != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    token = create_token({"sub": user.email, "user_id": user.id, "role": "admin"})
    return {"access_token": token, "token_type": "bearer"}


@app.post(
    "/tasks",
    response_model=TaskResponse,
    dependencies=[Depends(verify_token)],
)
def tasks(task: TaskCreate, db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    new_tasks = Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
    )
    db.add(new_tasks)
    db.commit()
    db.refresh(new_tasks)
    return new_tasks

@app.get("/readall", response_model=list[TaskResponse])
def readall(db:Session = Depends(get_db)):
    try:
        Read_all = db.query(Task).all()
        if not Task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Task Found"
            )
        return Read_all
    except:
        print("No Data Found")


@app.get("/readone/{id}", response_model=TaskResponse)
def readone(id:int , db:Session = Depends(get_db)):

    Read_one = db.query(Task).filter(Task.id == id).first()
    if not Read_one:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Task Found"
        )
    return Read_one


@app.put("/update/{id}" , response_model=TaskResponse)
def update(id: int, uptask: TaskCreate, db: Session = Depends(get_db)):

    update_one = db.query(Task).filter(Task.id == id).first()
    if not update_one:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No Task Found"
        )
    update_one.title = uptask.title
    update_one.description = uptask.description
    update_one.completed = uptask.completed
    
    db.commit()
    db.refresh(update_one)
    print("Task Updated Succefully")
    return update_one


@app.delete("/delone/{id}")
def delone(id:int , db:Session = Depends(get_db)):

    delete_one = db.query(Task).filter(Task.id == id).first()
    if not delete_one:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Task Found"
        )
    db.delete(delete_one)
    db.commit() 

    return {"message": "All tasks have been successfully deleted"}




@app.delete("/delall", status_code=status.HTTP_204_NO_CONTENT)
def delall(db: Session = Depends(get_db)):

    delete_all = db.query(Task).all()
    if not Task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No Task Found"
        )
    db.execute(delete(Task))
    db.commit()

    return {"message": "Selected tasks have been successfully deleted"}


