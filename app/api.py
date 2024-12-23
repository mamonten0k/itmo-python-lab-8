from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal, engine, Base
import models
from seed import seed_data
from schemas import Term as TermSchema, Relationship as RelationshipSchema

app = FastAPI()

# Initialize Database
def init_db():
    Base.metadata.create_all(bind=engine)
    db_session = SessionLocal()
    seed_data(db_session)
    db_session.close()

init_db()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/terms/", response_model=List[TermSchema])
def read_terms(db: Session = Depends(get_db)):
    terms = db.query(models.Term).all()
    return terms

@app.get("/relationships/", response_model=List[RelationshipSchema])
def read_relationships(db: Session = Depends(get_db)):
    relationships = db.query(models.Relationship).all()
    return relationships
