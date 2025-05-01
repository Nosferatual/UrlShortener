# crud.py

from sqlalchemy.orm import Session
from models import URL
from utils import generate_short_code
import schemas

def create_url(db: Session, original_url: str):
    short_code = generate_short_code()

    # Aynı kısa kod varsa yenisini üret
    while db.query(URL).filter(URL.short_code == short_code).first():
        short_code = generate_short_code()

    new_url = URL(original_url=original_url, short_code=short_code)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url
