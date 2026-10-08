# ajoad_islam_nishat_trip_planner_batch_12

Smart Group Trip Planner API: a REST backend built with **Python, Flask and SQLite** for Internship Batch 12.

## 1. Project Overview

A travel organization needs a backend to manage group trips. A trip has a destination, date range, budget, capacity, travelers, expenses and a lifecycle status. The API enforces business rules on the server side so that invalid operations are rejected:

- overbooking and duplicate participation
- overlapping trips for the same traveler
- overspending the trip budget
- invalid status transitions and edits on finished trips

Data is stored persistently in SQLite, so it survives application restarts.

## 2. Prerequisites

- Python 3.10 or newer (developed on Python 3.12)
- `pip` and the `venv` module
- Bash (Linux, macOS, or Git Bash/WSL on Windows) to use `run.sh`
- No manual database setup is required

## 3. Run From a Fresh Clone (recommended)

```bash
git clone https://github.com/ajoad-0139/ajoad_islam_nishat_trip_planner_batch_12.git
cd ajoad_islam_nishat_trip_planner_batch_12
./run.sh
```

`run.sh` will:

1. Create (or reuse) a local virtual environment in `./venv`
2. Install the dependencies from `requirements.txt`
3. Run the automated tests (`test_api.py`) and print the result
4. Create the SQLite database and tables if they do not exist
5. Start the API on **http://127.0.0.1:5000**

The tests always run before the server starts. If a test fails, a warning is printed and the server still starts, so the API stays usable. Two optional switches change this:

| Command | Effect |
|---|---|
| `STRICT_TESTS=1 ./run.sh` | Stop and do not start the server if any test fails |
| `SKIP_TESTS=1 ./run.sh` | Skip the tests and start the server immediately |

If you get "Permission denied", run `chmod +x run.sh` once.

Quick check:

```bash
curl http://127.0.0.1:5000/health
# {"status":"ok"}
```

## 4. Manual Run (fallback)

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Optional environment variables:

| Variable | Default | Purpose |
|---|---|---|
| `PORT` | `5000` | Port the server listens on |
| `APP_ENV` | `production` | Set to `development` to enable Flask debug mode |
| `LOG_LEVEL` | `INFO` | Logging level |
| `SQLALCHEMY_DATABASE_URI` | `sqlite:///trip_planner.db` | Database location |

## 4a. Run the Tests

```bash
source venv/bin/activate        # after ./run.sh or the manual setup above
python -m pytest -v test_api.py
```

The tests use Flask's built-in test client with a temporary SQLite database, so they do not touch `instance/trip_planner.db`. They cover:

| Endpoint | What is checked |
|---|---|
| `GET /health` | Returns 200 and `status: ok` |
| `POST` / `GET /api/v1/trips` | Create and retrieve a trip; invalid dates are rejected (400) |
| `POST /api/v1/trips/<id>/travelers` | Duplicate email (409), exact-full capacity and over-capacity (409) |
| `POST /api/v1/trips/<id>/expenses` | An expense equal to the remaining budget succeeds; one above it fails (409) |

## 5. API Endpoints

Base URL: `http://127.0.0.1:5000`

| Method | Endpoint | Purpose | Success |
|---|---|---|---|
| GET | `/health` | Application health | 200 |
| POST | `/api/v1/trips` | Create a trip | 201 |
| GET | `/api/v1/trips` | List trips | 200 |
| GET | `/api/v1/trips/<trip_id>` | Get one trip | 200 |
| PUT | `/api/v1/trips/<trip_id>` | Update a trip | 200 |
| DELETE | `/api/v1/trips/<trip_id>` | Delete a trip | 200 |
| POST | `/api/v1/trips/<trip_id>/travelers` | Add a traveler | 201 |
| DELETE | `/api/v1/trips/<trip_id>/travelers/<traveler_id>` | Remove a traveler | 200 |
| POST | `/api/v1/trips/<trip_id>/expenses` | Add an expense | 201 |
| PATCH | `/api/v1/trips/<trip_id>/status` | Change trip status | 200 |
| GET | `/api/v1/trips/<trip_id>/summary` | Calculated trip summary | 200 |

All responses are JSON. IDs are integers.

## 6. Example Requests and Responses

### Create a trip

```bash
curl -X POST http://127.0.0.1:5000/api/v1/trips \
  -H "Content-Type: application/json" \
  -d '{"destination":"Cox'"'"'s Bazar","start_date":"2026-10-20","end_date":"2026-10-23","budget":30000,"max_travelers":5}'
```

Response `201 Created`:

```json
{
  "id": 1,
  "destination": "Cox's Bazar",
  "start_date": "2026-10-20",
  "end_date": "2026-10-23",
  "budget": 30000.0,
  "max_travelers": 5,
  "status": "PLANNED"
}
```

### Update a trip

Fields you omit keep their current value.

```bash
curl -X PUT http://127.0.0.1:5000/api/v1/trips/1 \
  -H "Content-Type: application/json" \
  -d '{"max_travelers": 8}'
```

### Add a traveler

```bash
curl -X POST http://127.0.0.1:5000/api/v1/trips/1/travelers \
  -H "Content-Type: application/json" \
  -d '{"name":"Ayesha Rahman","email":"ayesha@example.com"}'
```

Response `201 Created`:

```json
{
  "trip": {
    "id": 1,
    "destination": "Cox's Bazar",
    "start_date": "2026-10-20",
    "end_date": "2026-10-23",
    "budget": 30000.0,
    "max_travelers": 5,
    "status": "PLANNED",
    "trip_id": 1,
    "traveler_count": 1,
    "available_seats": 4,
    "total_expense": 0.0,
    "remaining_budget": 30000.0
  },
  "traveler": { "id": 1, "name": "Ayesha Rahman", "email": "ayesha@example.com" }
}
```

### Add an expense

```bash
curl -X POST http://127.0.0.1:5000/api/v1/trips/1/expenses \
  -H "Content-Type: application/json" \
  -d '{"title":"Hotel","amount":12000}'
```

Response `201 Created`:

```json
{ "id": 1, "trip_id": 1, "title": "Hotel", "amount": 12000.0 }
```

### Trip summary

```bash
curl http://127.0.0.1:5000/api/v1/trips/1/summary
```

```json
{
  "trip_id": 1,
  "status": "PLANNED",
  "traveler_count": 1,
  "available_seats": 4,
  "total_expense": 12000.0,
  "remaining_budget": 18000.0
}
```

### Change status

```bash
curl -X PATCH http://127.0.0.1:5000/api/v1/trips/1/status \
  -H "Content-Type: application/json" \
  -d '{"status":"ONGOING"}'
```

### Error response format

Every error has the same shape:

```json
{
  "error": "TRIP_FULL",
  "message": "The trip has reached its maximum traveler capacity."
}
```

| HTTP status | When | Example `error` codes |
|---|---|---|
| 400 | Invalid or malformed input | `VALIDATION_ERROR`, `INVALID_JSON` |
| 404 | Unknown resource or route | `TRIP_NOT_FOUND`, `TRAVELER_NOT_FOUND`, `TRAVELER_NOT_IN_TRIP` |
| 409 | Business-rule conflict | `DUPLICATE_TRAVELER`, `TRIP_FULL`, `TRAVELER_TRIP_OVERLAP`, `BUDGET_EXCEEDED`, `TRIP_NOT_PLANNED`, `TRIP_NOT_ACCEPTING_EXPENSES`, `TRIP_LOCKED`, `INVALID_TRIP_UPDATE`, `INVALID_STATUS` |
| 500 | Unexpected server error | `INTERNAL_SERVER_ERROR` |

Failed operations never return a 2xx status.

## 7. Business Rules and Assumptions

| Rule | Behavior |
|---|---|
| BR-01 | `end_date` must be later than `start_date`. |
| BR-02 | `budget` must be greater than zero. |
| BR-03 | `max_travelers` must be greater than zero. |
| BR-04 | A traveler is identified by **email** (stored lowercase). The same email cannot join the same trip twice. |
| BR-05 | A trip never holds more travelers than `max_travelers` (the exact-full case is allowed). |
| BR-06 | A traveler cannot be in two trips with overlapping date ranges. Cancelled trips are ignored. Trips that share a boundary date are treated as overlapping. |
| BR-07 | Expense `amount` must be greater than zero. |
| BR-08 | Total expenses never exceed the budget. An expense equal to the remaining budget is allowed. A trip update cannot set the budget below the expenses already recorded. |
| BR-09 | `max_travelers` cannot be reduced below the current traveler count. |
| BR-10 | Travelers can be added only while the trip is `PLANNED`. |
| BR-11 | Expenses can be added only while the trip is `PLANNED` or `ONGOING`. |
| BR-12 / BR-13 | `COMPLETED` and `CANCELLED` trips cannot be edited, accept travelers or expenses, or change status. |
| BR-14 | Only these status transitions are valid. |

Lifecycle:

```
PLANNED  -> ONGOING   -> COMPLETED
PLANNED  -> CANCELLED
ONGOING  -> CANCELLED
```

Every other transition (including same-status and anything out of `COMPLETED` or `CANCELLED`) returns `409`.

Assumptions:

- A new trip always starts as `PLANNED`.
- A traveler record is created the first time an email is used and reused for later trips. The name of an existing traveler is not overwritten.
- Money values are stored as `Decimal` with 2 decimal places and returned as JSON numbers.
- `PUT` accepts a partial body; omitted fields keep their current value.
- Deleting a trip also deletes its expenses and traveler links.

## 8. Project Structure

```
.
├── run.sh                  # one-command start (venv + install + run)
├── run.py                  # application entry point
├── requirements.txt        # pinned dependencies (includes pytest)
├── test_api.py             # automated API tests (run by run.sh)
├── README.md
├── .gitignore
├── config.py               # configuration (database URI, log level)
├── create_app.py           # Flask application factory
├── setup_sqlalchemy.py     # SQLAlchemy setup and automatic table creation
├── app_logging.py          # logging and request access log
└── app/
    ├── models.py           # Trip, Traveler, Expense, trip_traveler tables
    ├── schemas.py          # pydantic request validation
    ├── errors.py           # custom exceptions and JSON error handler
    ├── utils.py            # overlap detection helper
    ├── routes/
    │   ├── health.py       # GET /health
    │   └── trips.py        # all /api/v1/trips endpoints
    ├── services/
    │   └── trip.py         # business rules
    └── repositories/
        └── trip.py         # database access
```

Request flow: **route** (parse and validate input) -> **service** (business rules) -> **repository** (SQLAlchemy queries) -> JSON response. All errors go through one global error handler.

## 9. How SQLite Is Initialized and Stored

- The database URI is `sqlite:///trip_planner.db`. With Flask-SQLAlchemy this creates the file `instance/trip_planner.db` inside the project.
- On every startup `create_app` calls `db.create_all()`, which creates any missing tables. No SQL has to be run manually.
- The `instance/` folder and `*.db` files are listed in `.gitignore`, so the database is never committed. A fresh clone creates a new empty database on first run.
- Data persists between restarts. To reset, stop the server and delete `instance/trip_planner.db`.

Tables: `trips`, `travelers`, `trip_traveler` (many-to-many link), `expenses`.

## 10. Known Limitations

- The trip list is not paginated.
- There are no automated tests yet. Behavior was checked manually with Postman and curl.
- `run.sh` needs a Bash shell. On Windows use Git Bash or WSL, or the manual run steps.
- The automated tests cover only four endpoints (health, trips, travelers, expenses). Status transitions, the summary and the update rules were checked manually with Postman and curl.