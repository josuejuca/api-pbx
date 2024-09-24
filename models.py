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
