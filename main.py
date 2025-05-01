from fastapi import FastAPI, Depends, responses
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request, Form
from fastapi.staticfiles import StaticFiles  # varsa

import models
import schemas
import crud

# HTML dosyaları için templates klasörü tanımı
templates = Jinja2Templates(directory="templates")
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/shorten", response_model=schemas.URLResponse)
def shorten_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    new_url = crud.create_url(db=db, original_url=url.original_url)
    return new_url

@app.get("/r/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    if url:
        return RedirectResponse(url.original_url)
    return {"error": "URL bulunamadı"}

@app.post("/shorten-url", response_class=HTMLResponse)
def post_form(request: Request, original_url: str = Form(...), db: Session = Depends(get_db)):
    new_url = crud.create_url(db=db, original_url=original_url)
    short_url = f"http://localhost:8000/r/{new_url.short_code}"
    return templates.TemplateResponse("index.html", {
        "request": request,
        "short_url": short_url
    })


