# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

import models, schemas, crud
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/extensions/", response_model=List[schemas.Extension], tags=["PBX-API (CRUD)"])
def read_extensions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    extensions = crud.get_extensions(db, skip=skip, limit=limit)
    return extensions

@app.get("/extensions/{extension_uuid}", response_model=schemas.Extension, tags=["PBX-API (CRUD)"])
def read_extension(extension_uuid: UUID, db: Session = Depends(get_db)):
    db_extension = crud.get_extension(db, extension_uuid)
    if db_extension is None:
        raise HTTPException(status_code=404, detail="Extension not found")
    return db_extension

@app.post("/extensions/", response_model=schemas.Extension, tags=["PBX-API (CRUD)"])
def create_extension(extension: schemas.ExtensionCreate, db: Session = Depends(get_db)):
    return crud.create_extension(db, extension)

@app.put("/extensions/{extension_uuid}", response_model=schemas.Extension, tags=["PBX-API (CRUD)"])
def update_extension(extension_uuid: UUID, extension: schemas.ExtensionUpdate, db: Session = Depends(get_db)):
    return crud.update_extension(db, extension_uuid, extension)

@app.delete("/extensions/{extension_uuid}", response_model=schemas.Extension, tags=["PBX-API (CRUD)"])
def delete_extension(extension_uuid: UUID, db: Session = Depends(get_db)):
    return crud.delete_extension(db, extension_uuid)


# Rota para atualizar apenas a senha da extensão
@app.put("/extensions/{extension_uuid}/password", response_model=schemas.Extension, tags=["GERÊNCIA"])
def update_password(extension_uuid: UUID, password_update: schemas.ExtensionUpdatePassword, db: Session = Depends(get_db)):
    db_extension = crud.update_extension_password(db, extension_uuid, password_update.new_password)
    if db_extension is None:
        raise HTTPException(status_code=404, detail="Extension not found")
    return db_extension

# Rota para desativar uma extensão
@app.put("/extensions/{extension_uuid}/deactivate", response_model=schemas.Extension, tags=["GERÊNCIA"])
def deactivate_extension(extension_uuid: UUID, db: Session = Depends(get_db)):
    db_extension = crud.deactivate_extension(db, extension_uuid)
    if db_extension is None:
        raise HTTPException(status_code=404, detail="Extension not found")
    return db_extension

# Rota para desativar uma extensão
@app.put("/extensions/{extension_uuid}/activate", response_model=schemas.Extension, tags=["GERÊNCIA"])
def activate_extension(extension_uuid: UUID, db: Session = Depends(get_db)):
    db_extension = crud.activate_extension(db, extension_uuid)
    if db_extension is None:
        raise HTTPException(status_code=404, detail="Extension not found")
    return db_extension