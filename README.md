# CodeCraftHub

A beginner-friendly REST API for managing online learning courses. Built with Python and Flask, CodeCraftHub stores course data in a simple JSON file and exposes standard HTTP endpoints so you can practice creating, reading, updating, and deleting resources—the core operations of any REST API.

---

## Table of Contents

1. [What is CodeCraftHub?](#what-is-codecrafthub)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [How to Run the Application](#how-to-run-the-application)
6. [Understanding REST APIs (Quick Intro)](#understanding-rest-apis-quick-intro)
7. [API Documentation](#api-documentation)
8. [Testing the API](#testing-the-api)
9. [Project Structure](#project-structure)
10. [Troubleshooting](#troubleshooting)
11. [Next Steps](#next-steps)

---

## What is CodeCraftHub?

CodeCraftHub is a small web service that lets you track courses you are learning (or teaching). Each course has a name, description, target completion date, and status.

Instead of using a database, this project stores everything in a file called `courses.json`. That keeps the project simple while still demonstrating how real APIs work:

- Clients send **HTTP requests** (GET, POST, PUT, DELETE)
- The server returns **JSON responses**
- Errors use standard **status codes** (200, 201, 400, 404, 500)

This project is designed for people who are learning REST APIs for the first time.

---

## Features

- **Create courses** — Add new courses with auto-generated IDs and timestamps
- **List all courses** — Retrieve every course in the system
- **Get one course** — Look up a single course by its ID
- **Update courses** — Change one or more fields (partial updates supported)
- **Delete courses** — Remove a course permanently
- **Course statistics** — View total course count and breakdown by status
- **Input validation** — Clear error messages for missing or invalid data
- **File-based storage** — No database setup required; data persists in `courses.json`
- **Auto-recovery** — Creates `courses.json` automatically if it does not exist

### Allowed course statuses

| Status         | Meaning                          |
|----------------|----------------------------------|
| `Not Started`  | Course has not been started yet  |
| `In Progress`  | Course is currently in progress  |
| `Completed`    | Course has been finished         |

---

## Prerequisites

Before you begin, make sure you have:

| Requirement | How to check | Notes |
|-------------|--------------|-------|
| **Python 3.8+** | `python --version` | Python 3.10 or newer is recommended |
| **pip** | `pip --version` | Comes with most Python installations |
| **A terminal** | — | Command Prompt, PowerShell, or Git Bash on Windows |
| **curl** (optional) | `curl --version` | For testing from the command line |

> **New to Python?** Download it from [python.org](https://www.python.org/downloads/). On Windows, check **"Add Python to PATH"** during installation.

---

## Installation

Follow these steps in order.

### Step 1: Get the project files

If you cloned the repository:

```bash
git clone <your-repo-url>
cd codecrafthub
```

Or open a terminal in the folder that contains `app.py`.

### Step 2: Create a virtual environment (recommended)

A virtual environment keeps this project's packages separate from other Python projects.

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

When the virtual environment is active, your terminal prompt usually shows `(venv)`.

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

This installs:

- **Flask** — the web framework that runs the API
- **Werkzeug** — Flask's underlying HTTP toolkit

### Step 4: Verify installation

```bash
pip show Flask
```

You should see version information for Flask 3.0.0.

---

## How to Run the Application

### Start the server

```bash
python app.py
```

You should see output similar to:

```text
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

The API is now available at:

```text
http://127.0.0.1:5000
```

`127.0.0.1` means "this computer" (localhost). Port `5000` is where Flask listens for requests.

### Stop the server

Press `Ctrl + C` in the terminal where the server is running.

### Keep the server running while testing

Leave the server terminal open. Open a **second terminal** to run test commands (curl, Postman, etc.).

---

## Understanding REST APIs (Quick Intro)

A **REST API** is a way for programs to talk to a server over HTTP. Each **endpoint** is a URL path combined with an HTTP **method**:

| Method   | Purpose        | Example in this project        |
|----------|----------------|--------------------------------|
| `GET`    | Read data      | List all courses               |
| `POST`   | Create data    | Add a new course               |
| `PUT`    | Update data    | Change a course's status       |
| `DELETE` | Remove data    | Delete a course                |

### Common HTTP status codes

| Code | Meaning        | When you see it here                    |
|------|----------------|-----------------------------------------|
| 200  | OK             | Successful GET, PUT, or DELETE          |
| 201  | Created        | Successful POST (new course created)    |
| 400  | Bad Request    | Invalid or missing data in your request |
| 404  | Not Found      | Course ID does not exist                |
| 500  | Server Error   | Problem reading or writing `courses.json` |

### What is JSON?

JSON (JavaScript Object Notation) is a text format for structured data. Example:

```json
{
  "name": "Python Basics",
  "status": "In Progress"
}
```

This API sends and receives JSON in request and response bodies.

---

## API Documentation

**Base URL:** `http://127.0.0.1:5000`

### Course object

When you create or retrieve a course, it looks like this:

```json
{
  "id": 1,
  "name": "Python Basics",
  "description": "Learn Python fundamentals",
  "target_date": "2026-12-31",
  "status": "Not Started",
  "created_at": "2026-06-26T12:00:00.000000Z"
}
```

| Field         | Type   | Set by   | Description                              |
|---------------|--------|----------|------------------------------------------|
| `id`          | number | Server   | Unique identifier (auto-generated)       |
| `name`        | string | Client   | Course title (required on create)        |
| `description` | string | Client   | Course description (required on create)  |
| `target_date` | string | Client   | Target date in `YYYY-MM-DD` format       |
| `status`      | string | Client   | One of the three allowed statuses        |
| `created_at`  | string | Server   | UTC timestamp when the course was created|

---

### 1. Create a course

**`POST /api/courses`**

Creates a new course. All four fields are required.

**Request body:**

```json
{
  "name": "Python Basics",
  "description": "Learn Python fundamentals",
  "target_date": "2026-12-31",
  "status": "Not Started"
}
```

**curl example:**

```bash
curl -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Python Basics\",\"description\":\"Learn Python fundamentals\",\"target_date\":\"2026-12-31\",\"status\":\"Not Started\"}"
```

**Success response:** `201 Created`

```json
{
  "id": 1,
  "name": "Python Basics",
  "description": "Learn Python fundamentals",
  "target_date": "2026-12-31",
  "status": "Not Started",
  "created_at": "2026-06-26T12:00:00.000000Z"
}
```

**Error response (missing fields):** `400 Bad Request`

```json
{
  "errors": [
    "Missing field: description",
    "Missing field: target_date",
    "Missing field: status"
  ]
}
```

---

### 2. Get all courses

**`GET /api/courses`**

Returns every course as a JSON array.

**curl example:**

```bash
curl http://127.0.0.1:5000/api/courses
```

**Success response:** `200 OK`

```json
[
  {
    "id": 1,
    "name": "Python Basics",
    "description": "Learn Python fundamentals",
    "target_date": "2026-12-31",
    "status": "Not Started",
    "created_at": "2026-06-26T12:00:00.000000Z"
  }
]
```

If no courses exist, you get an empty array: `[]`

---

### 3. Get course statistics

**`GET /api/courses/stats`**

Returns the total number of courses and a count for each status.

**curl example:**

```bash
curl http://127.0.0.1:5000/api/courses/stats
```

**Success response:** `200 OK`

```json
{
  "total": 3,
  "by_status": {
    "Completed": 1,
    "In Progress": 1,
    "Not Started": 1
  }
}
```

---

### 4. Get a course by ID

**`GET /api/courses/<id>`**

Returns a single course. Replace `<id>` with the course number (e.g. `1`).

**curl example:**

```bash
curl http://127.0.0.1:5000/api/courses/1
```

**Success response:** `200 OK` — returns the course object.

**Error response (not found):** `404 Not Found`

```json
{
  "error": "Course not found."
}
```

---

### 5. Update a course

**`PUT /api/courses/<id>`**

Updates an existing course. You can send **only the fields you want to change** (partial update).

**Request body (partial update example):**

```json
{
  "status": "In Progress"
}
```

**Request body (full update example):**

```json
{
  "name": "Advanced Python",
  "description": "Deep dive into Python",
  "target_date": "2027-01-15",
  "status": "Completed"
}
```

**curl example:**

```bash
curl -X PUT http://127.0.0.1:5000/api/courses/1 \
  -H "Content-Type: application/json" \
  -d "{\"status\":\"In Progress\"}"
```

**Success response:** `200 OK` — returns the updated course object.

**Error response (not found):** `404 Not Found`

```json
{
  "error": "Course not found."
}
```

**Error response (invalid date):** `400 Bad Request`

```json
{
  "errors": [
    "Field 'target_date' must be in YYYY-MM-DD format."
  ]
}
```

---

### 6. Delete a course

**`DELETE /api/courses/<id>`**

Permanently removes a course.

**curl example:**

```bash
curl -X DELETE http://127.0.0.1:5000/api/courses/1
```

**Success response:** `200 OK`

```json
{
  "deleted": {
    "id": 1,
    "name": "Python Basics",
    "description": "Learn Python fundamentals",
    "target_date": "2026-12-31",
    "status": "Not Started",
    "created_at": "2026-06-26T12:00:00.000000Z"
  }
}
```

**Error response (not found):** `404 Not Found`

```json
{
  "error": "Course not found."
}
```

---

### API quick reference

| Method   | Endpoint                  | Body required?      | Success code |
|----------|---------------------------|---------------------|--------------|
| `POST`   | `/api/courses`            | Yes (all 4 fields)  | 201          |
| `GET`    | `/api/courses`            | No                  | 200          |
| `GET`    | `/api/courses/stats`      | No                  | 200          |
| `GET`    | `/api/courses/<id>`       | No                  | 200          |
| `PUT`    | `/api/courses/<id>`       | Yes (1+ fields)     | 200          |
| `DELETE` | `/api/courses/<id>`       | No                  | 200          |

---

## Testing the API

You can test the API using **curl** (command line), **Postman**, or any HTTP client.

### Option A: curl (command line)

Make sure the server is running (`python app.py`), then open a second terminal.

**Windows PowerShell tip:** Use `curl.exe` and single quotes around JSON:

```powershell
curl.exe -X POST http://127.0.0.1:5000/api/courses `
  -H "Content-Type: application/json" `
  -d '{"name":"Test Course","description":"My first test","target_date":"2026-12-31","status":"Not Started"}'
```

**Show response headers and status code** — add `-i`:

```bash
curl -i http://127.0.0.1:5000/api/courses
```

**Pretty-print JSON** — pipe to Python:

```bash
curl http://127.0.0.1:5000/api/courses | python -m json.tool
```

### Option B: Postman or Insomnia

1. Create a new request.
2. Set the method (GET, POST, PUT, DELETE).
3. Enter the URL (e.g. `http://127.0.0.1:5000/api/courses`).
4. For POST/PUT: go to **Body** → **raw** → **JSON**, then paste your payload.
5. Click **Send**.

### End-to-end smoke test

Run these commands in order to verify everything works:

```bash
# 1. Create a course
curl -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Test Course\",\"description\":\"Smoke test\",\"target_date\":\"2026-12-31\",\"status\":\"Not Started\"}"

# 2. List all courses
curl http://127.0.0.1:5000/api/courses

# 3. Get course by ID (use the id from step 1)
curl http://127.0.0.1:5000/api/courses/1

# 4. Get statistics
curl http://127.0.0.1:5000/api/courses/stats

# 5. Update the course
curl -X PUT http://127.0.0.1:5000/api/courses/1 \
  -H "Content-Type: application/json" \
  -d "{\"status\":\"Completed\"}"

# 6. Delete the course
curl -X DELETE http://127.0.0.1:5000/api/courses/1

# 7. Confirm deletion (should return 404)
curl -i http://127.0.0.1:5000/api/courses/1
```

### Error scenario tests

Try these to see how validation works:

| Test                    | Command idea                                      | Expected result |
|-------------------------|---------------------------------------------------|-----------------|
| Missing fields on POST  | Send only `{"name": "Incomplete"}`                | 400 with errors |
| Invalid date            | `"target_date": "31-12-2026"`                     | 400 with errors |
| Invalid status          | `"status": "Almost Done"`                         | 400 with errors |
| Course not found        | `GET /api/courses/9999`                           | 404             |
| Empty name              | `"name": "   "`                                   | 400 with errors |
| Delete twice            | Delete the same ID twice                          | 404 on second   |

---

## Project Structure

```text
codecrafthub/
├── app.py              # Main Flask application (all API routes and logic)
├── courses.json        # Data file — list of courses (auto-created if missing)
├── requirements.txt    # Python package dependencies
├── README.md           # This file
└── venv/               # Virtual environment (created by you, not in git)
```

### File descriptions

| File               | Purpose |
|--------------------|---------|
| `app.py`           | Defines the Flask app, helper functions, validation, and all six API endpoints. Run this file to start the server. |
| `courses.json`     | Stores course data as a JSON array. The app reads from and writes to this file on every change. You can inspect it directly to see your data. |
| `requirements.txt` | Lists pinned dependency versions (`Flask`, `Werkzeug`) for reproducible installs. |
| `venv/`            | Optional folder created by `python -m venv venv`. Holds isolated Python packages. |

### How data flows

```text
Client (curl / Postman / browser)
        │
        ▼ HTTP request (GET, POST, PUT, DELETE)
   ┌─────────┐
   │  app.py │  ← Flask routes handle the request
   └────┬────┘
        │ read / write
        ▼
  courses.json  ← Persistent storage
```

1. A client sends an HTTP request to an endpoint in `app.py`.
2. `app.py` validates the input (for POST and PUT).
3. `app.py` loads courses from `courses.json`, performs the operation, and saves back.
4. `app.py` returns a JSON response with the appropriate status code.

---

## Troubleshooting

### `python` is not recognized

**Problem:** Windows cannot find Python.

**Fix:**
- Reinstall Python from [python.org](https://www.python.org/downloads/) and check **"Add Python to PATH"**.
- Or try `py app.py` instead of `python app.py`.

---

### `pip install` fails or permission denied

**Problem:** Installing packages fails.

**Fix:**
- Activate your virtual environment first (see [Installation](#installation)).
- On Windows, run: `python -m pip install -r requirements.txt`

---

### Port 5000 is already in use

**Problem:** Error like `Address already in use` or `Port 5000 is in use`.

**Fix:**
- Another program (or a previous Flask instance) is using port 5000.
- Stop the other process, or change the port in `app.py`:

```python
app.run(debug=True, port=5001)
```

Then use `http://127.0.0.1:5001` in your requests.

---

### curl returns HTML instead of JSON

**Problem:** You get a Flask error page or HTML response.

**Fix:**
- Check the URL path — it must start with `/api/courses`.
- For POST/PUT, include the header: `-H "Content-Type: application/json"`.
- Make sure the server is running.

---

### `Course not found` (404)

**Problem:** GET, PUT, or DELETE returns 404.

**Fix:**
- List all courses first: `curl http://127.0.0.1:5000/api/courses`
- Use an `id` that actually exists in the response.
- Remember: after you delete a course, that ID is gone.

---

### Validation errors (400)

**Problem:** POST or PUT returns `"errors": [...]`.

**Fix:**

| Error message | Solution |
|---------------|----------|
| `Missing field: ...` | Include all required fields on POST |
| `name must be a non-empty string` | Provide a non-empty `name` |
| `target_date must be in YYYY-MM-DD format` | Use dates like `2026-12-31`, not `12/31/2026` |
| `status must be one of: ...` | Use exactly `Not Started`, `In Progress`, or `Completed` |

---

### PowerShell curl issues with JSON

**Problem:** curl fails or sends malformed JSON on Windows.

**Fix:** Use `curl.exe` (not the PowerShell alias) and single quotes:

```powershell
curl.exe -X POST http://127.0.0.1:5000/api/courses -H "Content-Type: application/json" -d '{"name":"Test","description":"Desc","target_date":"2026-12-31","status":"Not Started"}'
```

---

### Changes do not appear / stale data

**Problem:** You updated data but do not see changes.

**Fix:**
- Make sure you are hitting the correct server (localhost, correct port).
- Check `courses.json` directly — it should reflect the latest data.
- If the file looks corrupted, stop the server, replace contents with `[]`, and restart.

---

### `Failed to read/write courses data` (500)

**Problem:** Server returns a 500 error.

**Fix:**
- Ensure `courses.json` is valid JSON (starts with `[` and ends with `]`).
- Check file permissions — the app needs read/write access to the project folder.
- Reset the file: stop the server, set `courses.json` to `[]`, restart.

---

## Next Steps

Once you are comfortable with CodeCraftHub, try extending it:

- Add a search or filter endpoint (e.g. courses by status)
- Add pagination to `GET /api/courses`
- Replace `courses.json` with SQLite or PostgreSQL
- Write automated tests with `pytest`
- Build a simple frontend that calls this API

---

## License

This project is intended for educational use. Check with your instructor or organization for licensing details.
