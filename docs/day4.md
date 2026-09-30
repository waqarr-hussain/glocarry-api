# Day 4 — SQLite Database Integration

## What I learned

Today I connected my Grocery App with a SQLite database.

I learned:

* What SQLite is
* How to create a database connection
* How to create a database table
* What a database schema is
* What a cursor is
* How to execute SQL commands
* How to insert data into a database
* How to select data from a database
* How to search using WHERE
* Difference between fetchone() and fetchall()
* Why commit() is used
* Why close() is used
* Parameterized SQL queries using ?

---

## 1. SQLite

SQLite is a lightweight database that can store application data in a database file.

In my project, the database file is:

`database.db`

I used Python's built-in sqlite3 module to work with SQLite.

```python
import sqlite3
```

---

## 2. Database Connection

I created a connection between Python and the SQLite database:

```python
connection = sqlite3.connect("database.db")
```

The connection allows Python to communicate with the database.

---

## 3. Creating the Products Table

I created a `products` table:

```sql
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER NOT NULL
)
```

The table contains:

| Column | Type    | Purpose           |
| ------ | ------- | ----------------- |
| id     | INTEGER | Unique product ID |
| name   | TEXT    | Product name      |
| price  | INTEGER | Product price     |

`PRIMARY KEY` identifies each product uniquely.

`AUTOINCREMENT` allows SQLite to generate the ID automatically.

`NOT NULL` means the value cannot be empty/null.

---

## 4. Cursor

I learned that a cursor is used to execute SQL commands and retrieve results from the database.

```python
cursor = connection.cursor()
```

The basic flow is:

Connection → Cursor → Execute SQL → Result

---

## 5. INSERT

I used `INSERT` to add a new product:

```python
cursor.execute(
    "INSERT INTO products (name, price) VALUES (?, ?)",
    (product.name, product.price)
)
```

For example:

```text
Bread
180
```

The product is inserted into the `products` table.

---

## 6. SELECT

To retrieve products, I used:

```python
cursor.execute("SELECT * FROM products")
```

`SELECT` is used to retrieve data.

`*` means all columns.

---

## 7. fetchall()

I used `fetchall()` when I wanted all results:

```python
products = cursor.fetchall()
```

It returns all rows returned by the query.

---

## 8. fetchone()

I used `fetchone()` when I wanted one matching result:

```python
product = cursor.fetchone()
```

For example:

```sql
SELECT * FROM products WHERE id = ?
```

This can return one specific product.

---

## 9. WHERE

`WHERE` is used to filter database results.

Example:

```sql
SELECT * FROM products WHERE id = ?
```

If the ID is `3`, the database searches for the product whose ID is 3.

I can also search by product name:

```sql
SELECT * FROM products WHERE name = ?
```

---

## 10. Parameterized Query

I learned that `?` can be used as a placeholder.

Example:

```python
cursor.execute(
    "SELECT * FROM products WHERE id = ?",
    (product_id,)
)
```

The value of `product_id` is supplied separately.

This allows the same query to be reused with different values.

---

## 11. commit()

After changing database data, I use:

```python
connection.commit()
```

`commit()` saves the changes to the database.

For example, after INSERT:

```python
cursor.execute(...)
connection.commit()
```

---

## 12. close()

After finishing database work, I close the connection:

```python
connection.close()
```

`close()` closes the current database connection.

It does not delete the database or its data.

---

## 13. API Testing

I tested my API using FastAPI Swagger UI.

Swagger URL:

`http://127.0.0.1:8000/docs`

I tested:

### Create Product

`POST /products`

Example:

```json
{
    "name": "Bread",
    "price": 180
}
```

### Get All Products

`GET /products`

### Get Product By ID

`GET /products/{product_id}`

Example:

`GET /products/1`

---

## 14. Persistence Test

I stopped the FastAPI server and started it again.

After restarting the server, the previously inserted product was still available.

This confirmed that the product was stored in the SQLite database instead of only existing temporarily in Python memory.

---

## What I understood

The complete database flow is:

```text
Python
   ↓
SQLite connection
   ↓
Cursor
   ↓
SQL command
   ↓
Database
   ↓
Result / Saved Data
```

For inserting data:

```text
Connection
   ↓
Cursor
   ↓
INSERT
   ↓
commit()
   ↓
close()
```

For reading data:

```text
Connection
   ↓
Cursor
   ↓
SELECT
   ↓
fetchone() / fetchall()
   ↓
close()
```

## Day 4 Result

I successfully connected my Grocery App to SQLite and tested storing and retrieving product data through FastAPI.
