# 🏨 Hotel Booking Dashboard & Data Provider

This project provides two Django-based services:

1️⃣ **Data Provider** — API for storing and retrieving hotel booking and cancellation events.  
2️⃣ **Dashboard** — API for generating monthly/daily booking summaries for hotels.

Both services are Dockerized, use PostgreSQL, and provide Swagger (OpenAPI) documentation for easy API exploration.

---

## 🚀 Features

### Data Provider
✅ POST /events — Create a new booking or cancellation event  
✅ GET /events — Retrieve events with filters:
- hotel_id
- date ranges (timestamp, night_of_stay)
- room_id
- booking status (1 = booking, 2 = cancellation)

---

### Dashboard
✅ GET /dashboard — Get summary stats:
- Monthly bookings for a year
- Daily bookings for a year  

Supports query params:
- `hotel_id`
- `period` = `month` or `day`
- `year`

---

### Tech stack
- Django 5.x
- Django REST Framework
- drf-yasg for Swagger/OpenAPI
- PostgreSQL
- Docker + Docker Compose

---

## 💡 Design decisions

- **Separate apps** for `data_provider` and `dashboard` to keep concerns clean.
- `original_event_id` stored to retain the source system's ID without clashing with Django’s primary key.
- Timestamps stored as timezone-aware UTC datetimes for consistency.
- Dockerization for easy deployment & reproducibility.
- Swagger integration for clear API contracts.
- **Pagination** — We decided **not to apply pagination on the `/dashboard/` API** because the output (aggregated stats) is limited in size by design (e.g., at most 12 monthly or ~365 daily records).  
  However, **the `/events/` API could return a large dataset** (e.g., 65,000+ records).  
  Since filtering by hotel, date, room, and status is supported, users are expected to filter data to manageable chunks.  
  👉 Pagination could easily be added using Django REST Framework’s pagination classes if scaling becomes an issue in production.
---

## ⚙️ Installation

### 🐳 Prerequisites
- Docker
- Docker Compose

---

### 🛠️ Steps

1️⃣ **Clone the repo**
```bash
git clone https://github.com/sanathbn27/Hotel_booking_app.git
cd Hotel_booking_app
```

2️⃣ **Build and start the containers**
```bash
docker-compose up --build
```
3️⃣ **Apply migrations**
```bash
docker-compose run web python manage.py migrate
```

## 🚀 How to use

### Access the app:
- **Data Provider API & Dashboard API:** [http://localhost:8000](http://localhost:8000)
- **Swagger UI:** [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

### Example queries:
```http
GET /events/?hotel_id=123&from=2022-01-01&to=2022-12-31
GET /dashboard/?hotel_id=123&period=month&year=2022
```

## Running Tests
```bash
docker-compose run web python manage.py test
```