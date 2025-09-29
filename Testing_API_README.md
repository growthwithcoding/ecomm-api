# 🛒 Ecommerce API Testing Guide

![Postman](https://img.shields.io/badge/Postman-Workspace-orange?logo=postman)
![API](https://img.shields.io/badge/API-Flask-blue?logo=flask)
![Tests](https://img.shields.io/badge/Tests-Positive%20%2F%20Negative-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

This guide documents how to test the **Ecommerce API** with Postman, including environment setup, happy-path tests, and negative/error-path tests.

---

## ⚙️ 1) Environment Setup in Postman
1. Import the environment: **Ecommerce API - Environment.postman_environment.json**  
2. Defines variables like `baseUrl`, `initDbToken`, and placeholders (`userId`, `productId`, `orderId`).  
3. Select the environment (top-right in Postman) so variables like `{{baseUrl}}` resolve correctly.  

---

## ✅ 2) Positive Tests (Happy Path)

1. **Setup: Reset Vars** → `GET /`  
   - Health ping and reset environment variables.  
2. **Health Check** → `GET /`  
   - Confirms API is alive and returns `status: ok`.  
3. **Init DB** → `POST /init-db`  
   - Creates DB tables using `initDbToken`.  
4. **Create User** → `POST /users`  
   - Creates a user and saves `userId`.  
5. **Create Product** → `POST /products`  
   - Creates a product and saves `productId`.  
6. **Create Order** → `POST /orders`  
   - Creates order tied to `userId`, saves `orderId`.  
7. **Add Product to Order** → `PUT /orders/{orderId}/add_product/{productId}`  
   - Adds product to order.  
8. **Get Products for Order** → `GET /orders/{orderId}/products`  
   - Retrieves products for order.  
9. **Remove Product from Order** → `DELETE /orders/{orderId}/remove_product/{productId}`  
   - Removes product from order.  
10. **Get Order by ID** → `GET /orders/{orderId}`  
    - Retrieves single order.  
11. **Get Orders for User** → `GET /orders/user/{userId}`  
    - Retrieves all orders for a user.  
12. **Delete Order** → `DELETE /orders/{orderId}`  
    - Deletes order and clears `orderId`.  

---

## ❌ 3) Negative Tests (Error Paths)

### 👤 Users
- Create missing email → **400**
- Create duplicate email → **409**
- Get user by id (not found) → **404**
- Delete user (not found) → **404**
- Create with wrong Content-Type → **400**
- Pagination bad params → **400**
- `PATCH /users` not allowed → **405**

### 📦 Products
- Create missing price → **400**
- Create negative price → **400**
- Get product by id (not found) → **404**

### 📑 Orders
- Create missing user_id → **400**
- Create bad date format → **400**
- Create with user not found → **404**
- Add product not found → **404**
- Add same product twice → **200 or 409**
- Remove product not in order → **404 or 200**
- Get order by id (not found) → **404**
- Get orders for missing user → **404 or 200 []**

---

## 🚀 Quick Run Order
1. **Select environment** (`ecomm-api`).  
2. Run the **Positive suite** (top to bottom).  
3. Run the **Negative suite**.  

---

## 📜 License
This project is licensed under the MIT License.  
