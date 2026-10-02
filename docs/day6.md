# Day 6 — HTTP Status Codes & HTTPException

## 1. Day 6 Goal

Aaj ka goal FastAPI API responses ko proper HTTP status codes ke saath handle karna tha.

Day 5 mein CRUD APIs complete ki gayi thin. Day 6 mein un APIs ko proper HTTP response behavior diya gaya.

Main concepts:

* HTTP Status Codes
* 200 OK
* 201 Created
* 404 Not Found
* HTTPException
* raise
* cursor.rowcount
* Error handling
* Swagger testing

---

# 2. HTTP Status Codes

HTTP status code server ki taraf se batata hai ke request ka result kya hua.

Examples:

* 200 = Request successfully complete
* 201 = New resource successfully created
* 404 = Requested resource nahi mila

---

# 3. GET — 200 OK

GET ka purpose data retrieve karna hai.

Example:

```python
@app.get("/products", status_code=200)
def get_products():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    connection.close()

    return products
```

Yahan:

```python
status_code=200
```

ka matlab hai ke products successfully retrieve hone par API `200 OK` return karegi.

---

# 4. GET Product by ID

```python
@app.get("/products/{product_id}", status_code=200)
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
```

Agar product mil jaye:

```text
200 OK
```

Agar product na mile:

```text
404 Not Found
```

---

# 5. HTTPException

FastAPI mein proper HTTP error return karne ke liye `HTTPException` use ki.

Import:

```python
from fastapi import FastAPI, HTTPException
```

Example:

```python
raise HTTPException(
    status_code=404,
    detail="Product not found"
)
```

Yahan:

* `raise` execution ko rokta hai
* `HTTPException` FastAPI ko error response banane kehta hai
* `status_code=404` HTTP status set karta hai
* `detail` error ka message hai

Response:

```json
{
    "detail": "Product not found"
}
```

HTTP status:

```text
404 Not Found
```

---

# 6. GET Product by Name

```python
@app.get("/products/name/{product_name}", status_code=200)
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
```

Product milne par:

```text
200 OK
```

Product na milne par:

```text
404 Not Found
```

---

# 7. POST — 201 Created

POST ka purpose new product create karna hai.

```python
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
```

Yahan:

```python
status_code=201
```

ka matlab hai:

```text
201 Created
```

Jab naya product successfully database mein create ho jaye.

---

# 8. PUT — 200 OK / 404 Not Found

PUT existing product ko update karta hai.

```python
@app.put("/products/{product_id}", status_code=200)
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
```

Successful update:

```text
200 OK
```

Product ID exist na kare:

```text
404 Not Found
```

---

# 9. cursor.rowcount

`cursor.rowcount` batata hai ke SQL operation se kitni rows affect hui hain.

Example:

```python
if cursor.rowcount == 0:
```

Agar value `0` hai to iska matlab hai ke koi product update nahi hua.

Is case mein:

```python
raise HTTPException(
    status_code=404,
    detail="Product not found"
)
```

execute hota hai.

---

# 10. DELETE — 200 OK / 404 Not Found

DELETE existing product ko database se remove karta hai.

```python
@app.delete("/products/{product_id}", status_code=200)
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
```

Successful deletion:

```text
200 OK
```

Product exist na kare:

```text
404 Not Found
```

---

# 11. Complete Status Code Table

| Operation           | Success | Error |
| ------------------- | ------: | ----: |
| GET all products    |     200 |     — |
| GET product by ID   |     200 |   404 |
| GET product by name |     200 |   404 |
| POST product        |     201 |     — |
| PUT product         |     200 |   404 |
| DELETE product      |     200 |   404 |

---

# 12. Important Difference: Response Body vs Status Code

API response ke do important parts hote hain:

### Response Body

Example:

```json
{
    "detail": "Product not found"
}
```

### HTTP Status Code

```text
404 Not Found
```

`404` response body ke andar zaroori nahi hota.

Status code HTTP response ka separate part hota hai.

---

# 13. Testing

Day 6 mein API ko Swagger UI se test kiya.

## Successful GET

Existing product ID use ki.

Expected:

```text
200 OK
```

## Failed GET

Non-existing ID:

```text
999
```

Response:

```json
{
    "detail": "Product not found"
}
```

HTTP status:

```text
404 Not Found
```

## POST

New product create kiya.

Expected:

```text
201 Created
```

## PUT

Existing product ko update kiya.

Expected:

```text
200 OK
```

Non-existing ID ke liye:

```text
404 Not Found
```

## DELETE

Existing product delete kiya.

Expected:

```text
200 OK
```

Non-existing ID ke liye:

```text
404 Not Found
```

---

# 14. What I Learned Today

Day 6 ke end par mujhe ye concepts samajh aaye:

1. HTTP status codes kya hote hain.
2. `200 OK` successful request ko represent karta hai.
3. `201 Created` new resource creation ko represent karta hai.
4. `404 Not Found` resource missing hone ko represent karta hai.
5. FastAPI mein `HTTPException` se proper error response create kiya ja sakta hai.
6. `raise` exception ko trigger karta hai.
7. `detail` error message provide karta hai.
8. `cursor.rowcount` se check kiya ja sakta hai ke UPDATE/DELETE ne koi row affect ki ya nahi.
9. Response body aur HTTP status code different cheezen hain.
10. Swagger aur browser Network tab se HTTP status verify kiya ja sakta hai.

---

# 15. Day 6 Result

Day 6 ke baad Glocarry API mein CRUD endpoints proper HTTP status codes aur error handling ke saath implement ho gaye.

Current API features:

* GET products
* GET product by ID
* GET product by name
* POST product
* PUT product
* DELETE product
* 200 OK
* 201 Created
* 404 Not Found
* HTTPException error handling
* SQLite database integration
* Swagger API testing
