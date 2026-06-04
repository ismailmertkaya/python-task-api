# ✅ Task Manager REST API — FastAPI

A fully-featured REST API for task management, built with **Python** and **FastAPI**. Features automatic interactive documentation at `/docs`.

## 🚀 Features
- Full CRUD with partial updates (PATCH)
- Filter tasks by status and priority
- Input validation via Pydantic models
- Auto-generated Swagger UI docs
- Unit tests with pytest

## 🛠️ Tech Stack
| Technology | Purpose |
|---|---|
| Python 3.11+ | Language |
| FastAPI | Web framework |
| Pydantic v2 | Data validation & schemas |
| Uvicorn | ASGI server |
| Pytest | Testing |

## ▶️ Getting Started

```bash
git clone https://github.com/YOUR_USERNAME/python-task-api.git
cd python-task-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload
```

Open your browser at **http://localhost:8000/docs** for the interactive API explorer.

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks` | Get all tasks |
| GET | `/tasks?completed=true` | Filter by status |
| GET | `/tasks?priority=3` | Filter by priority (1-3) |
| GET | `/tasks/{id}` | Get task by ID |
| POST | `/tasks` | Create new task |
| PATCH | `/tasks/{id}` | Partially update task |
| DELETE | `/tasks/{id}` | Delete task |
| GET | `/tasks/stats/summary` | Get stats |

## 🧪 Running Tests

```bash
pytest test_main.py -v
```

Expected output:
```
test_create_task      PASSED
test_get_all_tasks    PASSED
test_update_task      PASSED
test_delete_task      PASSED
test_filter_by_completed PASSED
test_stats            PASSED
```

## 📚 What I Learned
- REST API design with FastAPI
- Pydantic for data validation and serialization
- HTTP status codes (201 Created, 204 No Content, 404 Not Found)
- Writing unit tests for REST APIs
- Difference between PUT (full replace) and PATCH (partial update)
