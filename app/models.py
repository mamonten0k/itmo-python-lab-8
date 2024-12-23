from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Term(Base):
    __tablename__ = "terms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text, nullable=False)

class Relationship(Base):
    __tablename__ = "relationships"

    id = Column(Integer, primary_key=True, index=True)
    term_1_id = Column(Integer, ForeignKey("terms.id"))
    term_2_id = Column(Integer, ForeignKey("terms.id"))
    relation_type = Column(String)

    term_1 = relationship("Term", foreign_keys=[term_1_id], backref="related_from")
    term_2 = relationship("Term", foreign_keys=[term_2_id], backref="related_to")
