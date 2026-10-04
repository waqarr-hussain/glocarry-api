# Glocarry API — Day 8

## Response Models & API Validation

### Objective

Improve the Glocarry API by separating **input data** from **output data** and creating predictable, validated API responses.

---

## 1. Input Schema — `ProductCreate`

Used when the client sends product data to the API.

```python
class ProductCreate(BaseModel):
    name: str
    price: int
```

Example request:

```json
{
    "name": "Milk",
    "price": 250
}
```

The client does not provide `id`; the database generates it.

---

## 2. Response Schema — `ProductResponse`

Defines what the API sends back to the client.

```python
class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
```

Example:

```json
{
    "id": 1,
    "name": "Milk",
    "price": 250
}
```

### Key Concept

**Input and output should not always use the same schema.**

This becomes especially important later for:

* User registration/login
* Authentication
* Orders
* Payments
* AI APIs
* Sensitive data protection

---

## 3. `response_model`

FastAPI uses `response_model` to define and validate the API response.

```python
@router.get("/", response_model=list[ProductResponse])
```

This means:

> Return a list of products, and every product must follow `ProductResponse`.

This gives the API a predictable **contract** between the backend and frontend.

---

## 4. Database → API Response

SQLite returns rows as tuples:

```python
(1, "Milk", 250)
```

The API converts them into structured dictionaries:

```python
{
    "id": product[0],
    "name": product[1],
    "price": product[2]
}
```

Then FastAPI returns clean JSON.

### Important Backend Flow

```text
Client
  ↓
Request Schema
  ↓
FastAPI
  ↓
Database
  ↓
Dictionary
  ↓
Response Schema
  ↓
JSON Response
```

This request → database → response flow is a fundamental backend pattern that will be reused throughout the project.

---

## 5. CRUD API Completed

| Method | Endpoint                | Purpose          |
| ------ | ----------------------- | ---------------- |
| GET    | `/products/`            | Get all products |
| GET    | `/products/{id}`        | Get product      |
| GET    | `/products/name/{name}` | Search by name   |
| POST   | `/products/`            | Create product   |
| PUT    | `/products/{id}`        | Update product   |
| DELETE | `/products/{id}`        | Delete product   |

All endpoints were tested using **Swagger UI**.

---

## 6. Error Handling

Non-existing products return:

```text
404 Product not found
```

using:

```python
raise HTTPException(
    status_code=404,
    detail="Product not found"
)
```

This teaches an important REST API principle:

> APIs should communicate success and failure through appropriate HTTP status codes.

---

## 7. What I Learned

* Pydantic request schemas
* Pydantic response schemas
* `response_model`
* Input vs output validation
* API contracts
* SQLite tuple → dictionary → JSON
* CRUD API design
* HTTP error handling
* Swagger API testing
* Separation of application responsibilities

---

## 8. Why This Matters for the Future

Today's concepts are not limited to the product API.

The same architecture will later be used for:

```text
Products
   ↓
Users
   ↓
Authentication
   ↓
Cart
   ↓
Orders
   ↓
Payments
   ↓
AI Features
   ↓
Production APIs
```

The most important lesson of Day 8 is:

> **A professional API does not just make data available — it defines, validates, and controls how data enters and leaves the system.**

---

## Day 8 Status

**Development:** Completed
**CRUD Testing:** Completed
**Response Models:** Implemented
**Error Handling:** Tested
**Documentation:** Completed
**GitHub:** Ready for commit & push
