# Day 5 — CRUD APIs with FastAPI and SQLite

## 1. What I Learned

Today I learned how to perform CRUD operations using FastAPI and SQLite.

CRUD means:

* **C — Create** → POST
* **R — Read** → GET
* **U — Update** → PUT
* **D — Delete** → DELETE

---

## 2. GET — Read Products

GET API database se products read karti hai.

```python
@app.get("/products")
def get_products():

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()

    connection.close()

    return products
```

### Important Concepts

`SELECT * FROM products`

Database ke `products` table se tamam records leta hai.

`fetchall()`

Database se tamam matching records ko Python mein lata hai.

---

## 3. GET Product by ID

```python
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
```

### Important Concepts

`product_id`

URL se product ki ID receive karta hai.

Example:

```text
/products/1
```

Yahan `1` product ID hai.

`WHERE id = ?`

Sirf us product ko search karta hai jiski ID given hai.

`fetchone()`

Sirf ek record return karta hai.

---

## 4. POST — Create Product

POST API database mein naya product create karti hai.

```python
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
```

### Important Concepts

`INSERT INTO`

Database mein naya record add karta hai.

`commit()`

Database mein change permanently save karta hai.

---

## 5. PUT — Update Product

PUT API existing product ko update karti hai.

```python
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
        return {"message": "Product not found"}

    connection.close()

    return {
        "message": "Product updated successfully",
        "id": product_id,
        "name": product.name,
        "price": product.price
    }
```

### Important Concepts

`UPDATE`

Existing database record ko change karta hai.

Example:

```sql
UPDATE products
SET name = ?, price = ?
WHERE id = ?
```

`rowcount`

Batata hai ke SQL operation ne kitne records affect kiye.

Agar:

```text
rowcount = 0
```

to iska matlab product nahi mila.

---

## 6. DELETE — Delete Product

DELETE API database se product remove karti hai.

```python
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
        return {"message": "Product not found"}

    connection.close()

    return {
        "message": "Product deleted successfully",
        "id": product_id
    }
```

### Important Concepts

`DELETE FROM`

Database se record remove karta hai.

`WHERE id = ?`

Sirf specified ID wala product delete karta hai.

`commit()`

Delete ko database mein save karta hai.

---

## 7. CRUD Flow

Glocarry API ka CRUD flow:

```text
Client
   ↓
FastAPI
   ↓
API Endpoint
   ↓
SQLite Database
   ↓
SQL Query
   ↓
Response
```

CRUD:

```text
POST   → Create
GET    → Read
PUT    → Update
DELETE → Delete
```

---

## 8. Swagger Testing

Day 5 mein APIs ko FastAPI Swagger UI ke through test kiya.

Swagger URL:

```text
http://127.0.0.1:8000/docs
```

### Tested Operations

* GET all products
* GET product by ID
* GET product by name
* POST product
* PUT product
* DELETE product

PUT operation ko existing product par test kiya aur database mein successfully update verify kiya.

DELETE operation ko test kiya aur GET request ke through verify kiya ke deleted product database mein available nahi tha.

---

## 9. What I Learned Today

Day 5 mein maine seekha:

1. CRUD kya hota hai.
2. GET se database records read karna.
3. POST se new records create karna.
4. PUT se existing records update karna.
5. DELETE se records remove karna.
6. SQL `UPDATE` query.
7. SQL `DELETE` query.
8. `cursor.rowcount` ka use.
9. `commit()` ka importance.
10. Swagger se CRUD APIs test karna.

## Day 5 Status

**CRUD APIs: Completed ✅**

**Swagger Testing: Completed ✅**

**SQLite Integration: Completed ✅**

**Documentation: Completed ✅**
