# Day 7 — Professional FastAPI Project Structure

## 1. Day 7 Objective

The main objective of Day 7 was to refactor the Glocarry Grocery API from a single-file structure into a more organized and maintainable FastAPI project structure.

During Days 1–6, most of the application logic was placed inside `main.py`.

On Day 7, responsibilities were separated into different files and folders.

The main concepts covered were:

* Project structure
* Separation of Concerns
* FastAPI routers
* `APIRouter`
* Pydantic schemas
* Reusable database connections
* Python packages and `__init__.py`
* Router registration
* CRUD API organization
* API testing with Swagger UI
* HTTP 404 verification

---

# 2. Project Structure

The project structure after Day 7:

```text
glocarry app/
│
├── routers/
│   ├── __init__.py
│   └── products.py
│
├── database.py
├── schemas.py
├── main.py
├── glocarry.py
├── database.db
│
└── docs/
    ├── day4.md
    ├── day5.md
    ├── day6.md
    └── day7.md
```

Each important part of the application now has a specific responsibility.

---

# 3. Separation of Concerns

One of the most important concepts learned on Day 7 is **Separation of Concerns**.

Separation of Concerns means dividing an application into different components where each component has a specific responsibility.

Instead of putting everything into one large file, we separate:

```text
Application
    ↓
Routes
    ↓
Validation / Schemas
    ↓
Database Connection
    ↓
Database
```

This makes the application easier to:

* Understand
* Maintain
* Debug
* Test
* Extend
* Scale

This structure is commonly used in professional backend applications.

---

# 4. `main.py`

`main.py` is the main entry point of the FastAPI application.

Its responsibility is mainly to:

1. Create the FastAPI application.
2. Import the required routers.
3. Register those routers with the application.

The product-specific API logic should not need to stay inside `main.py`.

This keeps the main application file clean.

---

# 5. `routers/products.py`

The `products.py` file contains the Product-related API routes.

Product operations include:

* Create product
* Read products
* Update product
* Delete product

These operations represent CRUD:

```text
C → Create
R → Read
U → Update
D → Delete
```

The product router keeps all Product API endpoints together.

For example:

```text
GET     /products/
GET     /products/{product_id}
GET     /products/name/{product_name}
POST    /products/
PUT     /products/{product_id}
DELETE  /products/{product_id}
```

---

# 6. `APIRouter`

FastAPI provides `APIRouter` for organizing related API endpoints.

Instead of defining every route directly in `main.py`, we can create a router for a specific feature.

For example:

```python
router = APIRouter(
    prefix="/products",
    tags=["Products"]
)
```

## `prefix`

The prefix adds a common path to all routes inside the router.

If the prefix is:

```text
/products
```

then a route such as:

```python
@router.get("/")
```

becomes:

```text
GET /products/
```

## `tags`

The `tags` value organizes endpoints inside Swagger UI.

For example:

```python
tags=["Products"]
```

causes the Product endpoints to appear under the Products section in Swagger.

---

# 7. `schemas.py`

The `schemas.py` file contains Pydantic models used for request validation.

Example:

```python
from pydantic import BaseModel


class Product(BaseModel):
    name: str
    price: int
```

This model defines the expected structure of Product input.

The client must provide:

```json
{
    "name": "Milk",
    "price": 250
}
```

The schema tells FastAPI/Pydantic that:

* `name` should be a string.
* `price` should be an integer.

---

# 8. Why Use a Separate Schema File?

If the Product model remains inside `main.py`, the main file becomes larger as the application grows.

By moving schemas into `schemas.py`, validation models become organized separately.

Later, the application may contain models such as:

```text
Product
User
Order
Cart
Category
LoginRequest
```

Keeping schemas separately makes the project easier to manage.

---

# 9. `database.py`

The `database.py` file contains the reusable database connection function.

Example:

```python
import sqlite3


def get_connection():
    connection = sqlite3.connect("database.db")
    return connection
```

Instead of repeatedly writing:

```python
sqlite3.connect("database.db")
```

throughout the project, we can call:

```python
get_connection()
```

This reduces repeated code and centralizes database connection logic.

---

# 10. `routers/__init__.py`

The `__init__.py` file is placed inside the `routers` folder.

It allows the folder to be treated as a Python package and supports importing modules from that package.

The file can remain empty.

The important point is that the file exists:

```text
routers/
├── __init__.py
└── products.py
```

---

# 11. Router Registration

Creating a router is not enough.

The router must be connected to the main FastAPI application.

The general structure is:

```python
from routers.products import router as products_router

app.include_router(products_router)
```

This connects the Product router to the main FastAPI application.

The relationship becomes:

```text
main.py
   ↓
products router
   ↓
Product endpoints
```

---

# 12. Complete Request Flow

A Product API request now passes through several organized components.

For example, when creating a product:

```text
Client / Swagger
       ↓
POST /products/
       ↓
main.py
       ↓
Product Router
       ↓
Product Schema
       ↓
Database Connection
       ↓
SQLite Database
       ↓
Response
```

Each component performs its own responsibility.

---

# 13. CRUD Architecture

The Product router contains the four basic CRUD operations.

## Create

```text
POST /products/
```

Used to create a new product.

## Read

```text
GET /products/
GET /products/{product_id}
GET /products/name/{product_name}
```

Used to retrieve products.

## Update

```text
PUT /products/{product_id}
```

Used to update an existing product.

## Delete

```text
DELETE /products/{product_id}
```

Used to delete an existing product.

---

# 14. API Testing

After restructuring the application, all Product endpoints were tested through FastAPI Swagger UI.

Swagger UI was opened at:

```text
http://127.0.0.1:8000/docs
```

The following tests were completed.

---

## 14.1 GET All Products

Endpoint:

```text
GET /products/
```

Result:

Successful.

Existing products were returned from the SQLite database.

---

## 14.2 GET Product by ID

Endpoint:

```text
GET /products/{product_id}
```

Result:

Successful.

A specific product was retrieved using its ID.

---

## 14.3 GET Product by Name

Endpoint:

```text
GET /products/name/{product_name}
```

Result:

Successful.

A product was retrieved using its name.

---

## 14.4 POST Product

Endpoint:

```text
POST /products/
```

A new product was submitted through Swagger.

Example:

```json
{
    "name": "Orange Juice",
    "price": 300
}
```

Result:

Product was successfully created and saved to the database.

---

## 14.5 POST Database Verification

After creating the product,:

```text
GET /products/
```

was executed again.

The newly created product appeared in the returned product list.

This confirmed that the POST operation successfully stored the product in the database.

---

## 14.6 PUT Product

Endpoint:

```text
PUT /products/{product_id}
```

An existing product was updated.

Example:

```json
{
    "name": "Fresh Orange Juice",
    "price": 350
}
```

Result:

Product was successfully updated.

---

## 14.7 PUT Verification

After the update,:

```text
GET /products/{product_id}
```

was executed for the same product.

The updated product information was returned.

This confirmed that the PUT operation successfully modified the database record.

---

## 14.8 DELETE Product

Endpoint:

```text
DELETE /products/{product_id}
```

An existing product was deleted successfully.

---

## 14.9 404 Verification

After deletion, the deleted product was requested again using:

```text
GET /products/{product_id}
```

The API returned:

```json
{
    "detail": "Product not found"
}
```

with HTTP status code:

```text
404
```

This confirmed that the deleted product was no longer available.

---

# 15. HTTP Status Code Concept

HTTP status codes communicate the result of an HTTP request.

Important status codes learned:

| Status Code | Meaning                 |
| ----------- | ----------------------- |
| 200         | OK / Successful request |
| 201         | Resource created        |
| 400         | Bad Request             |
| 401         | Unauthorized            |
| 403         | Forbidden               |
| 404         | Resource not found      |
| 500         | Internal Server Error   |

For example:

```python
raise HTTPException(
    status_code=404,
    detail="Product not found"
)
```

The status code tells the client what happened, while `detail` provides additional information.

---

# 16. Why This Structure Is Better

The previous approach placed many responsibilities inside `main.py`.

The new structure separates those responsibilities.

### Before

```text
main.py
 ├── FastAPI
 ├── Schemas
 ├── Database
 ├── Routes
 └── CRUD logic
```

### After

```text
main.py
   │
   ├── routers/products.py
   │
   ├── schemas.py
   │
   └── database.py
```

This becomes especially useful when the application grows.

For example, later we may have:

```text
routers/
├── products.py
├── users.py
├── orders.py
├── cart.py
└── auth.py
```

Each router can handle a different feature.

---

# 17. Interview Concepts Learned

## Q1. Why use APIRouter?

`APIRouter` helps organize related FastAPI endpoints into separate modules.

---

## Q2. Why separate routers from main.py?

It keeps `main.py` clean and makes the application easier to maintain and scale.

---

## Q3. What is Separation of Concerns?

It is the practice of dividing an application into components where each component has a specific responsibility.

---

## Q4. Why create a schemas.py file?

It keeps Pydantic validation models separate from application and routing logic.

---

## Q5. Why create database.py?

It centralizes database connection logic and avoids repeating the same connection code throughout the application.

---

## Q6. What is **init**.py?

It is a Python package initialization file that helps Python treat a directory as a package and supports package-based imports.

---

## Q7. What does `prefix="/products"` do?

It adds `/products` to the routes defined inside the router.

---

## Q8. What does `tags=["Products"]` do?

It groups Product endpoints under the Products section in Swagger UI.

---

## Q9. What is CRUD?

CRUD stands for:

```text
Create
Read
Update
Delete
```

---

## Q10. What is the difference between a schema and a database?

A schema/model defines the expected structure and validation of data, while the database stores the actual data.

---

# 18. Day 7 Problems and Lessons

During Day 7, the application initially had an import/module issue while connecting the router structure.

The error involved the `routers` module not being recognized.

The project structure was then corrected by creating:

```text
routers/__init__.py
```

The file naming was also standardized:

```text
schemas.py
products.py
```

After the structure was corrected, the application successfully started with Uvicorn and Swagger UI loaded correctly.

This was an important practical lesson:

**File names, folder structure, Python imports, and package organization must match each other.**

---

# 19. Day 7 Final Result

By the end of Day 7:

* FastAPI application was successfully reorganized.
* Database connection was separated into `database.py`.
* Pydantic models were separated into `schemas.py`.
* Product routes were separated into `routers/products.py`.
* `routers/__init__.py` was created.
* Product router was connected to the main application.
* CRUD endpoints were tested.
* Database persistence was verified.
* Update functionality was verified.
* Delete functionality was verified.
* 404 error handling was verified.
* Swagger UI was used for API testing.

## Day 7 Status

**Completed successfully.**

The next stage is to study the architecture in depth and understand how the different files communicate with each other, including the relevant FastAPI and backend interview concepts.
