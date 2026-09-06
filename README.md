# AccuBuds

A point-of-sale system for a medical-marijuana dispensary. Employees log in with a 4-digit PIN, browse inventory, ring up sales, and the system tracks stock and patients automatically.

## Stack

- **Backend:** Django 5.1 + Django REST Framework, SQLite
- **Frontend:** React (Create React App)
- **Auth:** 4-digit employee PIN → DRF Token

## Layout

```
accubud/        Django project (settings, root urls)
inventory/      Product catalog (flower, edible, concentrate, topical)
patients/       Medical-cannabis patient records (medical card, prescription)
sales/          Sale transactions (auto-decrements inventory)
users/          CustomUser with login_pin field + PIN login endpoint
frontend/       React POS UI (Login → POSHome)
```

## Quick start

### 1. Backend (Django)

```bash
cd /home/judge/AccuBuds
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo --reset
python manage.py createsuperuser   # optional, for /admin/
python manage.py runserver 0.0.0.0:8000
```

The API is now live at `http://localhost:8000/api/`.

### 2. Frontend (React, in a separate terminal)

```bash
cd /home/judge/AccuBuds/frontend
npm install
npm start     # http://localhost:3000, proxies /api → :8000
```

Or build for production:

```bash
npm run build    # outputs to frontend/build/
```

Then `python manage.py runserver` will serve the React build from Django's static files config.

## Demo credentials (after `seed_demo`)

| Username     | Password  | PIN  | Role        |
|--------------|-----------|------|-------------|
| techjuan     | demo1234  | 1234 | Owner       |
| manager      | demo1234  | 9999 | Manager     |
| budtender1   | demo1234  | 0420 | Budtender   |

## API endpoints

| Method | Path                              | Purpose                          |
|--------|-----------------------------------|----------------------------------|
| POST   | `/api/login/`                     | Employee PIN login → returns DRF token |
| POST   | `/api/logout/`                    | Invalidate a token               |
| POST   | `/api/token/`                     | Username/password → token (alt)  |
| GET    | `/api/products/`                  | List products                    |
| POST   | `/api/sales/process_sale/`        | Atomic sale: validates stock, decrements inventory, logs sale |
| GET    | `/api/patients/`                  | List patients                    |
| GET    | `/api/users/`                     | List users                       |
| GET    | `/admin/`                         | Django admin (back office)       |

### Sample login

```bash
curl -X POST http://localhost:8000/api/login/ \
    -H 'Content-Type: application/json' \
    -d '{"pin": "1234", "terminal": "420"}'
# → {"token":"...","user_id":1,"username":"techjuan","terminal":"420"}
```

### Sample sale

```bash
TOKEN=...
curl -X POST http://localhost:8000/api/sales/process_sale/ \
    -H "Authorization: Token $TOKEN" \
    -H 'Content-Type: application/json' \
    -d '{"product_id":1,"patient_id":1,"user_id":1,"quantity":1,"terminal_number":"420"}'
```

## What's intentionally minimal

- Single dispensary / no multi-location tenancy yet
- No payment processor integration (the "Credit Card / Gift Card / Fast Cash" buttons are UI stubs)
- No receipt printing
- The patient picker in the POS UI is hardcoded to patient id 1 — a real picker is a follow-up

See the commit history for the original Create React App scaffolding that was used as the starting point.
