# Routes & Endpoints Reference

CineBook is a server-rendered application, so most endpoints return HTML.
This document lists every route, its method, auth requirement and behaviour.
A machine-readable health endpoint is provided for monitoring.

## Conventions

- 🔓 = public · 🔒 = authentication required
- CSRF tokens are required on all `POST` requests (provided automatically in
  forms via `{{ form.hidden_tag() }}` / `csrf_token()`).

## Public (`main`)

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| GET | `/` | 🔓 | Landing page with features and seat-class pricing. |
| GET | `/about` | 🔓 | Project background and changelog summary. |
| GET | `/healthz` | 🔓 | **JSON** health check → `{"status": "ok"}` (HTTP 200). |

## Authentication (`auth`)

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| GET/POST | `/auth/signup` | 🔓 | Register a new account. Redirects to dashboard on success. |
| GET/POST | `/auth/login` | 🔓 | Log in with username **or** email. Returns 401 on bad credentials. Honours a safe local `?next=` redirect. |
| POST | `/auth/logout` | 🔒 | Log out the current user. |

### `POST /auth/signup` — fields

| Field | Rules |
| --- | --- |
| `first_name`, `last_name` | required, ≤ 64 chars |
| `username` | required, 3–64 chars, `[A-Za-z0-9_.-]`, unique |
| `email` | required, valid email, unique |
| `phone` | required, `^\+?[0-9\s\-]{7,15}$` |
| `password` | required, ≥ 8 chars |
| `confirm` | must equal `password` |

### `POST /auth/login` — fields

| Field | Rules |
| --- | --- |
| `identifier` | username or email |
| `password` | required |

## Bookings (`bookings`)

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| GET | `/dashboard/` | 🔒 | Current user's bookings (paginated) + stats. `?page=N`. |
| GET/POST | `/dashboard/new` | 🔒 | Create a booking. Computes total from seat class × seats. |
| POST | `/dashboard/<id>/cancel` | 🔒 | Cancel a booking. **403** if it isn't yours, **404** if missing. |

### `POST /dashboard/new` — fields

| Field | Rules |
| --- | --- |
| `movie_name` | required, ≤ 120 chars |
| `seat_class` | one of `AC Premium`, `AC Balcony`, `First Class`, `Second Class` |
| `seats` | integer 1–20 |
| `show_time` | datetime-local (`YYYY-MM-DDTHH:MM`) |
| `snacks` | optional, ≤ 200 chars |

## Seat pricing (per seat)

| Class | Price (₹) |
| --- | --- |
| AC Premium | 350 |
| AC Balcony | 280 |
| First Class | 180 |
| Second Class | 120 |

## Error pages

| Status | When |
| --- | --- |
| 403 | Accessing a resource you don't own. |
| 404 | Unknown route or missing record. |
| 500 | Unhandled server error (rolls back the DB session). |

## Example: health check

```bash
curl -s http://127.0.0.1:5000/healthz
# {"status":"ok"}
```
