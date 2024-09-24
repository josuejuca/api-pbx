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

# Esquema para atualização de senha
class ExtensionUpdatePassword(BaseModel):
    new_password: str