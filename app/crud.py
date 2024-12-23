from sqlalchemy.orm import Session
import models, schemas

def get_all_terms(db: Session):
    return db.query(models.Term).all()

def get_term_by_name(db: Session, name: str):
    return db.query(models.Term).filter(models.Term.name == name).first()

def create_term(db: Session, term: schemas.TermCreate):
    db_term = models.Term(name=term.name, description=term.description)
    db.add(db_term)
    db.commit()
    db.refresh(db_term)
    return db_term

def delete_term(db: Session, name: str):
    term = get_term_by_name(db, name)
    if term:
        db.delete(term)
        db.commit()
        return True
    return False

def get_all_relationships(db: Session):
    return db.query(models.Relationship).all()

def create_relationship(db: Session, relationship: schemas.RelationshipCreate):
    db_relationship = models.Relationship(
        term_1_id=relationship.term_1_id,
        term_2_id=relationship.term_2_id,
        relation_type=relationship.relation_type,
    )
    db.add(db_relationship)
    db.commit()
    db.refresh(db_relationship)
    return db_relationship