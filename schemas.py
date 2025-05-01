from pydantic import BaseModel

class URLBase(BaseModel):
    original_url: str  # Kullanıcının verdiği uzun link

class URLResponse(URLBase):
    short_code: str

    class Config:
        orm_mode = True
