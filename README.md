
# Weblog 📜

A simple blog backend API built with Django and DRF, allowing users to register, log in using JWT, share their own blogs, and comment on others' posts.

---

## 🚀 Features

* JWT Authentication (Login/Register)
* Blog CRUD functionality
* Commenting system on blog posts
* Role-based permissions (admin, owner)
* Full test coverage using `pytest`
* Swagger/OpenAPI documentation

---

## 💠 Technologies Used

* **Python**
* **Django**
* **Django REST Framework (DRF)**
* **JWT Authentication (SimpleJWT)**
* **Swagger / drf-spectacular**
* **Pytest**

---

## 📆 Setup Instructions

1. **Clone the project:**

   ```bash
   git clone https://github.com/yourusername/weblog.git
   cd weblog
   ```

2. **Create virtual environment & install dependencies:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Apply migrations:**

   ```bash
   python manage.py migrate
   ```

4. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

---

## 🧺s Running Tests

All unit and integration tests are written using `pytest`.

To run tests:

```bash
pytest .
```

Tests are organized per app inside the `tests/` directories.

---

## 📄 API Documentation

After running the server, you can access the interactive API docs at:

```
http://127.0.0.1:8000/api/schema/swagger-ui/
```

This is powered by `drf-spectacular` and auto-generates docs from views and serializers.

---

## 📁 Requirements

You can install all necessary packages using the included `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 🔒 Permissions

* Only authenticated users can create blogs or comments.
* Only blog owners or admins can edit/delete their content.
* Admins can manage all users and view all blogs/comments.

---

## ✅ Project Status

This is a backend-only prototype of a blog system and is fully functional for development/testing purposes. Frontend is not included.

---

## 🧑‍💻 Author

Created by **Farzam Ghavami** – feel free to contribute or fork.

---

## 📜 License

This project is open-source and available under the MIT License.
