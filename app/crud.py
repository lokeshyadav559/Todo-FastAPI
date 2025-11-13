from sqlalchemy.orm import Session
from app import models, schemas

def create(db: Session, todo: schemas.TodoCreate):
    db_todo = models.Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def list(db: Session):
    return db.query(models.Todo).all()

def get(db: Session, id: int):
    return db.query(models.Todo).filter(models.Todo.id == id).first()

def update(db: Session, id: int, todo: schemas.TodoUpdate):
    db_todo = get(db, id)
    if db_todo:
        for key, value in todo.dict(exclude_unset=True).items():
            setattr(db_todo, key, value)
        db.commit()
        db.refresh(db_todo)
    return db_todo

def mark_complete(db: Session, id: int):
    db_todo = get(db, id)
    if db_todo:
        db_todo.done = True
        db.commit()
        db.refresh(db_todo)
    return db_todo

def delete(db: Session, id: int):
    db_todo = get(db, id)
    if db_todo:
        db.delete(db_todo)
        db.commit()
        return True
    return False
