from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    price: int


class ProductResponse(BaseModel):
    id: int
    name: str
    price: int