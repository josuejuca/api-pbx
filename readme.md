### Estrutura do Projeto

1. **Criação da Estrutura de Diretórios**
   ```
   fastapi-fusionpbx/
   ├── main.py  # Arquivo principal da FastAPI
   ├── models.py  # Modelos de dados (Pydantic e SQLAlchemy)
   ├── database.py  # Configuração da conexão com o banco de dados
   ├── crud.py  # Funções de CRUD (Create, Read, Update, Delete)
   ├── schemas.py  # Schemas Pydantic para validação de dados
   └── requirements.txt  # Dependências do projeto
   ```

2. **Instalar as Dependências**
   Vamos usar `FastAPI`, `SQLAlchemy` e `psycopg2`. Crie um ambiente virtual e instale as dependências:

   ```bash
   mkdir fastapi-fusionpbx
   cd fastapi-fusionpbx
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   pip install fastapi uvicorn sqlalchemy psycopg2 pydantic
   ```

   Crie um arquivo `requirements.txt` com o seguinte conteúdo:

   ```
   fastapi
   uvicorn
   sqlalchemy
   psycopg2
   pydantic
   ```

3. **Configuração do Banco de Dados (`database.py`)**
   Este arquivo irá configurar a conexão com o banco de dados PostgreSQL.

   ```python
   # database.py
   from sqlalchemy import create_engine
   from sqlalchemy.ext.declarative import declarative_base
   from sqlalchemy.orm import sessionmaker

   DATABASE_URL = "postgresql://api:Josue191203#@pbx.josuejuca.com:5432/fusionpbx"

   engine = create_engine(DATABASE_URL)
   SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   Base = declarative_base()

   # Dependência para obter a sessão do banco de dados
   def get_db():
       db = SessionLocal()
       try:
           yield db
       finally:
           db.close()
   ```

4. **Modelos e Schemas (`models.py` e `schemas.py`)**
   Vamos definir os modelos de dados para representar a tabela `v_extensions`.

   - `models.py`:
   ```python
   # models.py
   from sqlalchemy import Column, String, Integer, Boolean, Text
   from sqlalchemy.dialects.postgresql import UUID
   from database import Base

   class Extension(Base):
       __tablename__ = "v_extensions"
       
       extension_uuid = Column(UUID(as_uuid=True), primary_key=True, index=True)
       domain_uuid = Column(UUID(as_uuid=True), index=True)
       extension = Column(String, index=True)
       number_alias = Column(String, nullable=True)
       password = Column(String, nullable=True)
       accountcode = Column(String, nullable=True)
       effective_caller_id_name = Column(String, nullable=True)
       effective_caller_id_number = Column(String, nullable=True)
       outbound_caller_id_name = Column(String, nullable=True)
       outbound_caller_id_number = Column(String, nullable=True)
       enabled = Column(Boolean, default=True)
       description = Column(Text, nullable=True)
   ```

   - `schemas.py`:
   ```python
   # schemas.py
   from pydantic import BaseModel
   from typing import Optional
   from uuid import UUID

   class ExtensionBase(BaseModel):
       extension: Optional[str]
       number_alias: Optional[str]
       password: Optional[str]
       accountcode: Optional[str]
       effective_caller_id_name: Optional[str]
       effective_caller_id_number: Optional[str]
       outbound_caller_id_name: Optional[str]
       outbound_caller_id_number: Optional[str]
       enabled: Optional[bool]
       description: Optional[str]

   class ExtensionCreate(ExtensionBase):
       extension: str
       password: str

   class ExtensionUpdate(ExtensionBase):
       pass

   class Extension(ExtensionBase):
       extension_uuid: UUID
       domain_uuid: UUID

       class Config:
           orm_mode = True
   ```

5. **Funções CRUD (`crud.py`)**
   Vamos criar funções para as operações de criar, ler, atualizar e excluir extensões.

   ```python
   # crud.py
   from sqlalchemy.orm import Session
   from models import Extension
   from schemas import ExtensionCreate, ExtensionUpdate
   from uuid import UUID

   def get_extensions(db: Session, skip: int = 0, limit: int = 100):
       return db.query(Extension).offset(skip).limit(limit).all()

   def get_extension(db: Session, extension_uuid: UUID):
       return db.query(Extension).filter(Extension.extension_uuid == extension_uuid).first()

   def create_extension(db: Session, extension: ExtensionCreate):
       db_extension = Extension(**extension.dict())
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
   ```

6. **API Principal (`main.py`)**
   Este arquivo é o ponto de entrada da FastAPI.

   ```python
   # main.py
   from fastapi import FastAPI, Depends, HTTPException
   from sqlalchemy.orm import Session
   from typing import List
   from uuid import UUID

   import models, schemas, crud
   from database import engine, get_db

   models.Base.metadata.create_all(bind=engine)

   app = FastAPI()

   @app.get("/extensions/", response_model=List[schemas.Extension])
   def read_extensions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
       extensions = crud.get_extensions(db, skip=skip, limit=limit)
       return extensions

   @app.get("/extensions/{extension_uuid}", response_model=schemas.Extension)
   def read_extension(extension_uuid: UUID, db: Session = Depends(get_db)):
       db_extension = crud.get_extension(db, extension_uuid)
       if db_extension is None:
           raise HTTPException(status_code=404, detail="Extension not found")
       return db_extension

   @app.post("/extensions/", response_model=schemas.Extension)
   def create_extension(extension: schemas.ExtensionCreate, db: Session = Depends(get_db)):
       return crud.create_extension(db, extension)

   @app.put("/extensions/{extension_uuid}", response_model=schemas.Extension)
   def update_extension(extension_uuid: UUID, extension: schemas.ExtensionUpdate, db: Session = Depends(get_db)):
       return crud.update_extension(db, extension_uuid, extension)

   @app.delete("/extensions/{extension_uuid}", response_model=schemas.Extension)
   def delete_extension(extension_uuid: UUID, db: Session = Depends(get_db)):
       return crud.delete_extension(db, extension_uuid)
   ```

7. **Executar a API**

   Inicie o servidor FastAPI com o `uvicorn`:

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

8. **Testar a API**

   - Acesse `http://localhost:8000/docs` para ver a documentação interativa da API.
   - Use os endpoints para listar, criar, atualizar e excluir extensões.
