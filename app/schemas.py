from pydantic import BaseModel
from typing import List, Optional

class TermBase(BaseModel):
    name: str
    description: str

class Term(TermBase):
    id: int

    class Config:
        orm_mode = True

class RelationshipBase(BaseModel):
    relation_type: str

class Relationship(RelationshipBase):
    id: int
    term_1_id: int
    term_2_id: int

    term_1: Optional[Term]
    term_2: Optional[Term]

    class Config:
        orm_mode = True
