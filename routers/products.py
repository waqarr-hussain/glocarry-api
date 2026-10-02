from fastapi import APIRouter, HTTPException
from schemas import Product
from database import get_connection


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# GET - All Products
@router.get("/", status_code=200)
def get_products():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    connection.close()

    return products


# GET - Product by ID
@router.get("/{product_id}", status_code=200)
def get_product(product_id: int):
    connection = get_connection()
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
@router.get("/name/{product_name}", status_code=200)
def get_product_by_name(product_name: str):
    connection = get_connection()
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
@router.post("/", status_code=201)
def create_product(product: Product):
    connection = get_connection()
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
@router.put("/{product_id}", status_code=200)
def update_product(product_id: int, product: Product):
    connection = get_connection()
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
@router.delete("/{product_id}", status_code=200)
def delete_product(product_id: int):
    connection = get_connection()
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