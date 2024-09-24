# crud.py
from sqlalchemy.orm import Session
from models import Extension
from schemas import ExtensionCreate, ExtensionUpdate
from uuid import uuid4, UUID

def get_extensions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Extension).offset(skip).limit(limit).all()

def get_extension(db: Session, extension_uuid: UUID):
    return db.query(Extension).filter(Extension.extension_uuid == extension_uuid).first()

def create_extension(db: Session, extension: ExtensionCreate):
    # Gerar um UUID para o novo registro
    db_extension = Extension(
        extension_uuid=uuid4(),  # Gera um UUID único
        domain_uuid="664882d5-e861-47aa-b57b-9128631a5837",  # Adapte aqui para o UUID correto do domínio
        **extension.dict()
    )
    db.add(db_extension)
    db.commit()
    db.refresh(db_extension)
    return db_extension

def update_extension(db: Session, extension_uuid: UUID, extension: ExtensionUpdate):
    db_extension = get_extension(db, extension_uuid)
    if db_extension:
        for key, value in extension.dict(exclude_unset=True).items():
            setattr(db_extension, key, value)
        db.commit()
        db.refresh(db_extension)
    return db_extension

def delete_extension(db: Session, extension_uuid: UUID):
    db_extension = get_extension(db, extension_uuid)
    if db_extension:
        db.delete(db_extension)
        db.commit()
    return db_extension


# Função para atualizar apenas a senha de uma extensão
def update_extension_password(db: Session, extension_uuid: UUID, new_password: str):
    db_extension = db.query(Extension).filter(Extension.extension_uuid == extension_uuid).first()
    if db_extension:
        db_extension.password = new_password
        db.commit()
        db.refresh(db_extension)
    return db_extension

# Função para desativar uma extensão
def deactivate_extension(db: Session, extension_uuid: UUID):
    db_extension = db.query(Extension).filter(Extension.extension_uuid == extension_uuid).first()
    if db_extension:
        db_extension.enabled = False
        db.commit()
        db.refresh(db_extension)
    return db_extension


# Função para ativar uma extensão
def activate_extension(db: Session, extension_uuid: UUID):
    db_extension = db.query(Extension).filter(Extension.extension_uuid == extension_uuid).first()
    if db_extension:
        db_extension.enabled = True
        db.commit()
        db.refresh(db_extension)
    return db_extension

