# 🪙 Currency Converter API

A Django REST API that converts between CLP, COP, and PEN using cryptocurrency prices from [Buda.com](https://www.buda.com). The conversion uses the best intermediary crypto available (e.g., BTC).

---

## 🚀 Features

- Convert between fiat currencies (CLP, COP, PEN)
- Uses market data from Buda.com
- Selects best intermediary cryptocurrency automatically
- Swagger UI for easy testing and documentation
- Fully containerized with Docker

---

## 🧱 Project Structure

```
.
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── manage.py
├── requirements.txt
├── buda_test/
├── conversion/
└── db.sqlite3
```

---

## 🐳 Running the App with Docker

> Make sure you have Docker and Docker Compose installed.

```bash
# 1. Build the container
docker-compose build

# 2. Start the app
docker-compose up
```

Visit the app at:
```
http://localhost:8000
```

---

## 📘 API Documentation (Swagger)

Once running, visit:

```
http://localhost:8000/swagger/
```

There you can:
- Try out requests live
- See schema and example inputs
- View expected responses

---

## 🔁 Example Conversion Request

**Endpoint:**
```
POST /convert/
```

**Request Body:**

```json
{
  "from_currency": "CLP",
  "to_currency": "PEN",
  "amount": 10000
}
```

**Response Example:**

```json
{
  "converted_amount": 39.1,
  "intermediate_currency": "BTC"
}
```

---

## 🧪 Running Tests

To run the test suite (inside Docker):

```bash
docker-compose run web python manage.py test
```

---

## 📦 Requirements

- Python 3.13
- Django
- Django REST Framework
- drf-yasg (Swagger UI)
- Docker

Install locally with:

```bash
pip install -r requirements.txt
```

---

## 🔒 Notes

- This project currently uses SQLite for simplicity (not for production use).
- No authentication is enabled — it’s an open demo endpoint.

---

## ✨ TODO (optional)

- Add PostgreSQL support
- Deploy to a cloud provider
- Add support for more fiat currencies
- Add caching layer for market data

---

## License

MIT — feel free to use and adapt.
