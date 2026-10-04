from fastapi import APIRouter, HTTPException

from database import get_connection
from schemas import ProductCreate, ProductResponse


# Products ke liye router create kar rahe hain
router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# --------------------------------
# GET ALL PRODUCTS
# --------------------------------

@router.get("/", response_model=list[ProductResponse])
def get_products():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, name, price FROM products")
    products = cursor.fetchall()

    connection.close()

    return [
        {
            "id": product[0],
            "name": product[1],
            "price": product[2]
        }
        for product in products
    ]


# --------------------------------
# GET PRODUCT BY ID
# --------------------------------

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, name, price FROM products WHERE id = ?",
        (product_id,)
    )

    product = cursor.fetchone()

    connection.close()

    if product:
        return {
            "id": product[0],
            "name": product[1],
            "price": product[2]
        }

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )


# --------------------------------
# GET PRODUCT BY NAME
# --------------------------------

@router.get("/name/{product_name}", response_model=ProductResponse)
def get_product_by_name(product_name: str):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, name, price FROM products WHERE name = ?",
        (product_name,)
    )

    product = cursor.fetchone()

    connection.close()

    if product:
        return {
            "id": product[0],
            "name": product[1],
            "price": product[2]
        }

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )


# --------------------------------
# CREATE PRODUCT
# --------------------------------

@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(product: ProductCreate):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO products (name, price) VALUES (?, ?)",
        (product.name, product.price)
    )

    connection.commit()

    product_id = cursor.lastrowid

    connection.close()

    return {
        "id": product_id,
        "name": product.name,
        "price": product.price
    }


# --------------------------------
# UPDATE PRODUCT
# --------------------------------

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductCreate
):

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
        "id": product_id,
        "name": product.name,
        "price": product.price
    }


# --------------------------------
# DELETE PRODUCT
# --------------------------------

@router.delete("/{product_id}")
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