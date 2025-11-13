from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import engine, get_db
import asyncio

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/todos", status_code=201)
async def create(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create(db, todo)

@app.get("/todos")
async def list_todos(db: Session = Depends(get_db)):
    return crud.list(db)

@app.get("/todos/{id}")
async def get(id: int, db: Session = Depends(get_db)):
    todo = crud.get(db, id)
    if not todo:
        raise HTTPException(404, "Not found")
    return todo

@app.put("/todos/{id}")
async def update(id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    updated = crud.update(db, id, todo)
    if not updated:
        raise HTTPException(404, "Not found")
    return updated

@app.patch("/todos/{id}/complete")
async def mark_complete(id: int, db: Session = Depends(get_db)):
    todo = crud.mark_complete(db, id)
    if not todo:
        raise HTTPException(404, "Not found")
    return todo

@app.delete("/todos/{id}", status_code=204)
async def delete(id: int, db: Session = Depends(get_db)):
    if not crud.delete(db, id):
        raise HTTPException(404, "Not found")
