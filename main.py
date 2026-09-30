from fastapi import FastAPI
from pydantic import BaseModel

class Product(BaseModel):
    id : int
    name: str
    price: float

app = FastAPI()


# Home route
@app.get("/")
def home():
    return {"message": "Welcome to my Grocery App!"}


# Get all products
@app.get("/products")
def get_products():
    products = [
        {"id": 1, "name": "Milk", "price": 250},
        {"id": 2, "name": "Eggs", "price": 300},
        {"id": 3, "name": "Bread", "price": 180},
        {"id": 4, "name": "Rice", "price": 350},
        {"id": 5, "name": "Apples", "price": 400},
        {"id": 6, "name": "Bananas", "price": 200},
        {"id": 7, "name": "Chicken", "price": 700},
        {"id": 8, "name": "Potatoes", "price": 150}
    ]

    return products


# Get one specific product by ID
@app.get("/products/{product_id}")
def get_product(product_id: int):


    products = [
        {"id": 1, "name": "Milk", "price": 250},
        {"id": 2, "name": "Eggs", "price": 300},
        {"id": 3, "name": "Bread", "price": 180},
        {"id": 4, "name": "Rice", "price": 350},
        {"id": 5, "name": "Apples", "price": 400},
        {"id": 6, "name": "Bananas", "price": 200},
        {"id": 7, "name": "Chicken", "price": 700},
        {"id": 8, "name": "Potatoes", "price": 150}
    ]

    for product in products:
        if product["id"] == product_id:
            return product
        
        
    return {"message":"product not found"}     




@app.post("/products")
def create_product(product: Product):

    return product

from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()


# Product ka structure
class Product(BaseModel):
    name: str
    price: int


# Database aur table create karna
connection = sqlite3.connect("database.db")

connection.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER NOT NULL
)
""")

connection.commit()
connection.close()


# -------------------------
# GET: Saare products
# -------------------------

@app.get("/products")
def get_products():

    connection = sqlite3.connect("database.db")

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()

    connection.close()

    return products


# -------------------------
# GET: ID se ek product
# -------------------------

@app.get("/products/{product_id}")
def get_product(product_id: int):

    connection = sqlite3.connect("database.db")

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    )

    product = cursor.fetchone()

    connection.close()

    if product:
        return product

    return {"message": "Product not found"}


# -------------------------
# POST: Naya product add
# -------------------------

@app.post("/products")
def create_product(product: Product):

    connection = sqlite3.connect("database.db")

    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO products (name, price) VALUES (?, ?)",
        (product.name, product.price)
    )

    connection.commit()

    connection.close()

    return {
        "message": "Product created successfully",
        "name": product.name,
        "price": product.price
    }