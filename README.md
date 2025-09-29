# 🛒 E-Commerce API with Flask, SQLAlchemy, Marshmallow & MySQL

[![Author](https://img.shields.io/badge/author-growthwithcoding-blue)](https://github.com/growthwithcoding)
![Flask](https://img.shields.io/badge/Flask-3.x-lightgrey)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-red)
![Marshmallow](https://img.shields.io/badge/Marshmallow-3.x-blue)
![MySQL](https://img.shields.io/badge/MySQL-9.x-yellow)

This repository implements the **Relational Databases & REST API Development Project**.  
It delivers a fully functional **E-Commerce API** with proper relational models, Marshmallow validation, and Postman test collections (positive + negative).

---

## 📌 Overview
- **Framework**: Flask  
- **ORM**: SQLAlchemy  
- **Serialization & Validation**: Marshmallow  
- **Database**: MySQL  
- **Testing**: Postman Collections (positive & negative flows) + MySQL Workbench

The API manages **Users, Orders, and Products**, with:
- One-to-Many: One User → Many Orders  
- Many-to-Many: Orders ↔ Products (via association table with composite PK to prevent duplicates)

---

## 🗂 Project Structure

```
ecomm-api/
├─ app.py                     # main Flask app with models, schemas, endpoints
├─ requirements.txt           # Python dependencies
├─ .env                       # DB credentials & config (local only)
├─ postman/
│  ├─ Ecommerce-API-Environment.postman_environment.json
│  ├─ Ecommerce-API-Positive.postman_collection.json
│  └─ Ecommerce-API-Negative.postman_collection.json
└─ README.md
```

---

## 🗃 Database Models

**User**
- `id` (PK, auto)
- `name` (str)
- `address` (str)
- `email` (unique str)

**Order**
- `id` (PK, auto)
- `order_date` (DateTime, ISO required)
- `user_id` (FK → User.id)

**Product**
- `id` (PK, auto)
- `product_name` (str)
- `price` (float, non-negative)

**Order_Product** *(association)*
- `order_id` (FK → Order.id)
- `product_id` (FK → Product.id)
- **Composite PK** to prevent duplicate product per order

---

## 📦 Marshmallow Schemas
- **UserSchema**  
- **OrderSchema** (with `include_fk=True` so `user_id` is included)  
- **ProductSchema** (validates `price >= 0`)  

---

## 🚀 Endpoints

### Users
- `GET /users` → all users (paginated)  
- `GET /users/<id>` → single user  
- `POST /users` → create (unique email enforced)  
- `PUT /users/<id>` → update  
- `DELETE /users/<id>` → delete  

### Products
- `GET /products`  
- `GET /products/<id>`  
- `POST /products`  
- `PUT /products/<id>`  
- `DELETE /products/<id>`  

### Orders
- `POST /orders` → create new order (`user_id`, `order_date`)  
- `PUT /orders/<order_id>/add_product/<product_id>` → add product (no duplicates)  
- `DELETE /orders/<order_id>/remove_product/<product_id>` → remove product  
- `GET /orders/<order_id>/products` → list products in an order  
- `GET /orders/user/<user_id>` → list all orders for a user  

### Bonus
- `GET /orders/<id>/total` → order total  
- `GET /orders/user/<user_id>/summary` → order count + totals  

---

## 🧪 Testing

### ✅ Positive Tests
Located in `postman/Ecommerce-API-Positive.postman_collection.json`.  
Covers the **happy path**: creating a user, product, order, adding/removing products, and querying relations.

### ❌ Negative Tests
Located in `postman/Ecommerce-API-Negative.postman_collection.json`.  
Covers **error paths**: missing fields, duplicate email, bad date format, invalid IDs, wrong content-type, duplicate adds, etc.

### Environment
`postman/Ecommerce-API-Environment.postman_environment.json` defines:
- `baseUrl` (default `http://127.0.0.1:5000`)  
- `initDbToken` (set to `dev-init-ok`)  
- variables for `userId`, `productId`, `orderId`, `uniqueName`, `uniqueEmail`, `isoDate`  

### Workflow
1. Run **Positive collection** top-to-bottom.  
2. Run **Negative collection** to verify error handling.  
3. Confirm in **MySQL Workbench** that the DB is populated correctly.  

---

## ⚙️ Setup

```powershell
# create venv
python -m venv venv
.venv\Scripts\Activate.ps1

# install deps
pip install -r requirements.txt

# set env (Windows PowerShell)
$env:FLASK_APP="app.py"
$env:FLASK_ENV="development"
$env:SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://root:<PASSWORD>@127.0.0.1:3306/ecommerce_api"

# run API
python .app.py
```

---

## 📊 Presentation Checklist
- Show DB tables exist in Workbench (`user`, `order`, `product`, `order_product`).  
- Run **Positive collection** (user → product → order → add product → remove → query).  
- Run **Negative collection** (missing email, bad date, duplicate, 404s).  
- Point out **JSON error handlers** keep responses consistent.  
- Mention **pagination** in `/users` and `/products`.  

---

## 🧾 Assessment Criteria
- **Database Models** (30%) – relationships set up correctly  
- **API Functionality** (40%) – endpoints work (CRUD, associations)  
- **Serialization & Validation** (20%) – Marshmallow schemas & validation  
- **Code Quality** (10%) – clean, organized code with comments  

---

## 📚 Resources
- [Flask Docs](https://flask.palletsprojects.com/)  
- [Flask-SQLAlchemy Docs](https://flask-sqlalchemy.palletsprojects.com/)  
- [Marshmallow Docs](https://marshmallow.readthedocs.io/)  
- [MySQL Connector Docs](https://dev.mysql.com/doc/connector-python/en/)  
