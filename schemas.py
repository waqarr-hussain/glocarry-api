from pydantic import BaseModel


# Product ke input data ke rules
class Product(BaseModel):
    name: str
    price: int