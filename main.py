from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()


# Product data ke rules
class Product(BaseModel):
    name: str
    price: int


# GET - All Products
@app.get("/products")
def get_products():

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()

    connection.close()

    return products


# GET - Product by ID
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

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )


# GET - Product by Name
@app.get("/products/name/{product_name}")
def get_product_by_name(product_name: str):

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM products WHERE name = ?",
        (product_name,)
    )

    product = cursor.fetchone()

    connection.close()

    if product:
        return product

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )


# POST - Create Product
@app.post("/products", status_code=201)
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


# PUT - Update Product
@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product):

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE products SET name = ?, price = ? WHERE id = ?",
        (product.name, product.price, product_id)
    )

    connection.commit()

    if cursor.rowcount == 0:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    connection.close()

    return {
        "message": "Product updated successfully",
        "id": product_id,
        "name": product.name,
        "price": product.price
    }


# DELETE - Delete Product
@app.delete("/products/{product_id}")
def delete_product(product_id: int):

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM products WHERE id = ?",
        (product_id,)
    )

    connection.commit()

    if cursor.rowcount == 0:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    connection.close()

    return {
        "message": "Product deleted successfully",
        "id": product_id
    }