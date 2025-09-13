# 🛒 E-commerce API (Flask + SQLAlchemy + Marshmallow + MySQL)

> Because who *doesn’t* want to spin up a mini-Amazon in their terminal?

---

## 🚀 Overview

Welcome to my **Relational Databases & REST API Project**!  
This bad boy is built with **Flask**, **Flask-SQLAlchemy**, **Flask-Marshmallow**, and **MySQL**.  

Here’s what it does (besides making you look like a backend wizard 🧙‍♂️):

- Manages **Users**, **Orders**, and **Products**.  
- Handles **relationships** like a pro:  
  - One **User** → Many **Orders**  
  - Many **Orders** ↔ Many **Products** (via an association table that refuses duplicate products in the same order).  
- Uses **Marshmallow Schemas** for validation + serialization.  
- Gives you **CRUD endpoints** for Users & Products, plus all the juicy Order operations.  
- Stores everything in a **MySQL database** (not SQLite — we’re doing this the grown-up way).  

---

## 🎯 Learning Objectives (a.k.a. Why This Exists)

✔️ **Database Design** – Build relational models with SQLAlchemy + MySQL  
✔️ **API Development** – REST endpoints that don’t make you cry  
✔️ **Serialization** – Marshmallow makes your JSON pretty *and* safe  
✔️ **Testing** – Postman + MySQL Workbench to prove it actually works  

---

## 🗂 Database Models

### 👤 User
- `id` → Integer, primary key, auto-increment  
- `name` → String  
- `address` → String  
- `email` → **Unique** String  

### 📦 Product
- `id` → Integer, primary key, auto-increment  
- `product_name` → String  
- `price` → Float (≥ 0)  

### 🧾 Order
- `id` → Integer, primary key, auto-increment  
- `order_date` → DateTime (required on create)  
- `user_id` → FK → `users.id`  

### 🔗 OrderProduct (association table)
- `order_id` → FK → `orders.id`  
- `product_id` → FK → `products.id`  
- Composite PK on (`order_id`, `product_id`) → no duplicates, sorry hoarders  

---

## 🧩 Relationships

- **User → Orders** (1 to ∞)  
- **Order ↔ Products** (∞ to ∞ via `order_product`)  
- Cascade delete on `User → Orders` so you don’t end up with ghost orders 👻  

---

## 📦 Schemas (Marshmallow Magic)

- **UserSchema**: name, email (must contain `@`), address.  
- **ProductSchema**: product_name, price (≥ 0).  
- **OrderSchema**: includes `user_id` (yep, `include_fk=True`) and nests products on dump.  

Validation included. No more “email: pizza” disasters. 🍕  

---

## 🔧 Endpoints

### Health / Setup
- `GET /` → sanity check (`{"status":"ok"}` if not on fire)  
- `POST /init-db` → create tables  
  - ⚠️ **Dev only**! If Flask isn’t in debug, send header: `X-Init-Token: <INIT_DB_TOKEN>`  

### 👤 User Endpoints
- `GET /users?page=1&per_page=20` → list users (with pagination metadata)  
- `GET /users/<id>` → get user by ID  
- `POST /users` → create user (`{name, email, address}`)  
- `PUT /users/<id>` → update user  
- `DELETE /users/<id>` → delete user (bye + cascade orders)  

### 📦 Product Endpoints
- `GET /products?page=1&per_page=20` → list products (with pagination metadata)  
- `GET /products/<id>` → get product by ID  
- `POST /products` → create product (`{product_name, price}`)  
- `PUT /products/<id>` → update product  
- `DELETE /products/<id>` → delete product  

### 🧾 Order Endpoints
- `POST /orders` → create order (`{user_id, order_date}`)  
- `GET /orders/<id>` → get single order (products embedded) — returns JSON 404 `"Order not found"` if missing  
- `PUT /orders/<order_id>/add_product/<product_id>` → add product to order (no duplicates)  
- `DELETE /orders/<order_id>/remove_product/<product_id>` → remove product from order  
- `DELETE /orders/<order_id>` → delete entire order (returns `{ "message": "Order deleted" }`)  
- `GET /orders/user/<user_id>` → get all orders for a user  
- `GET /orders/<order_id>/products` → get products in a specific order  

---

## 🛠️ Setup Guide

### 1) Clone the repo
```bash
git clone <your-repo-url>
cd ecommerce-api
```

### 2) Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Mac/Linux
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```

### 4) Configure `.env`
```ini
DB_USER=ecom_api_user
DB_PASS=Password123!
DB_HOST=127.0.0.1
DB_NAME=ecommerce_api
# Optional: protect /init-db outside debug mode
INIT_DB_TOKEN=dev-init-ok
```

### 5) Make MySQL start on boot (Windows)
- Open **services.msc** → find **MySQL93** → **Properties** → set **Startup type: Automatic** → **Start**.  
- Verify **Running** in MySQL Workbench.

### 6) Run the app
```bash
set FLASK_APP=app.py
flask run
```
👉 Visit [http://localhost:5000](http://localhost:5000) and you should see:
```json
{"status":"ok"}
```

---

## 🧪 Testing (Postman)

### Import the provided files
- **Collection:** `postman/Ecommerce-API.postman_collection.json`  
- **Environment:** `postman/Ecommerce-API-Environment.postman_environment.json`  
- Select the **ecomm-api** environment.

### Run order
1. **Setup: Reset Vars** (clears `userId`, `productId`, `orderId` and seeds a unique email)  
2. Health Check  
3. Init DB  
4. Create User  
5. Create Product  
6. Create Order  
7. Add Product to Order  
8. Get Products for Order  
9. Remove Product from Order  
10. Get Order by ID  
11. Get Orders for User  
12. Delete Order (clears `orderId` so reruns don’t point at a ghost)

### Reruns without headaches
- The collection generates a **unique email** on each run, so `POST /users` won’t 409.  
- `Setup: Reset Vars` clears IDs before each run.  
- `Delete Order` automatically clears `orderId` after success.

---

## 🧯 Error Semantics (what your API returns)

- `400 Bad Request` — validation errors (e.g., missing `order_date`, negative `price`).  
- `404 Not Found` — resource id doesn’t exist (JSON: `{ "error": "..." }`).  
- `409 Conflict` — unique/constraint violation (e.g., duplicate `email`). Use a new email or rely on the collection’s unique pre-script.

---

## 💻 Sample cURL (quick smoke)

```bash
curl -s http://localhost:5000/
curl -s -X POST http://localhost:5000/users -H "Content-Type: application/json" -d '{"name":"Ada","email":"ada@example.com","address":"London"}'
curl -s -X POST http://localhost:5000/products -H "Content-Type: application/json" -d '{"product_name":"Keyboard","price":99.99}'
curl -s -X POST http://localhost:5000/orders -H "Content-Type: application/json" -d '{"user_id":1,"order_date":"2025-09-06"}'
curl -s -X PUT http://localhost:5000/orders/1/add_product/1
curl -s http://localhost:5000/orders/1/products
```

---

## 👩‍💻 Author

**Austin Carlson**  
Coding Temple Software Engineering Bootcamp Student  

*(Yes, I built an API instead of online shopping. Proud?)* 🎉  

---

## 📚 Works Cited

- [Flask Documentation](https://flask.palletsprojects.com/) — the microframework that makes Python web dev actually fun  
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) — ORM magic, but for Flask  
- [Marshmallow](https://marshmallow.readthedocs.io/) — turns messy Python objects into beautiful JSON  
- [marshmallow-sqlalchemy](https://marshmallow-sqlalchemy.readthedocs.io/) — because we’re lazy and don’t want to write boilerplate schemas  
- [MySQL Connector/Python](https://dev.mysql.com/doc/connector-python/en/) — the DB bridge holding it all together  
- [python-dotenv](https://pypi.org/project/python-dotenv/) — secrets management for people who don’t hardcode passwords 😉
