from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import crud, models
from database import SessionLocal, engine
import os

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root(request: Request, db: Session = Depends(get_db)):
    urls = db.query(models.URL).all()
    return templates.TemplateResponse("index.html", {"request": request, "urls": urls})

@app.post("/shorten")
def create_short_url(request: Request, original_url: str = Form(...), db: Session = Depends(get_db)):
    crud.create_url(db, original_url)
    return RedirectResponse("/", status_code=303)
@app.post("/clear")
def clear_all_urls(db: Session = Depends(get_db)):
    db.query(models.URL).delete()
    db.commit()
    return RedirectResponse("/", status_code=303)

