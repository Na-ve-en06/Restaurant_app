# 🍽️ Restaurant App Backend – FastAPI Project

A secure, modular, and production-ready backend built using **FastAPI**, **PostgreSQL**, and **JWT authentication**, designed for a restaurant-based application with user management, address support, and authentication features.

---

## 🚀 Features

- ✅ User Registration and Login with JWT Authentication
- 🔐 Password Hashing (bcrypt)
- 🧾 Address Management (multiple addresses with `is_default` support)
- 👤 Admin and Regular User Roles
- 🛡️ Protected Routes with OAuth2 + Bearer Tokens
- 🔧 Environment-based Configuration (`.env`)
- 🧪 Auto-generated Swagger API Docs

---

## 🛠️ Tech Stack

| Layer        | Tech                             |
|--------------|----------------------------------|
| Backend      | [FastAPI](https://fastapi.tiangolo.com) |
| Database     | [PostgreSQL](https://www.postgresql.org) |
| Auth         | OAuth2, JWT, Passlib (bcrypt)     |
| Environment  | python-dotenv + Pydantic Settings |
| Docs         | Swagger UI (auto from FastAPI)    |

---

## 📁 Project Structure

restaurant_app_demo/
├── app/
│ ├── routers/
│ │ ├── auth.py
│ │ ├── user.py
│ │ ├── cart.py
│ │ └── menu.py
│ ├── config.py
│ ├── DB.py
│ ├── main.py
│ ├── oauth2.py
│ ├── schemas.py
│ └── utils.py
├── .env
├── .gitignore
└── README.md
