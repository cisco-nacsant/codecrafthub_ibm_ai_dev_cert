from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

# ----------------------------
# Configuration and constants
# ----------------------------

# File where courses are stored. The app will auto-create this file if it doesn't exist.
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'courses.json')

# Allowed statuses for a course
ALLOWED_STATUSES = {"Not Started", "In Progress", "Completed"}

# ----------------------------
# Helper functions
# ----------------------------

def ensure_data_file():
    """
    Ensure the JSON data file exists.
    If the file is missing, create it and initialize with an empty list [].
    """
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f, indent=2)

def load_courses():
    """
    Load the list of courses from the JSON file.
    Returns a list (empty list if file is empty or invalid).
    """
    ensure_data_file()
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                # If file content is not a list, treat as empty
                return []
    except json.JSONDecodeError:
        # If JSON is corrupted, treat as empty to keep app running
        return []
    except Exception as e:
        # Propagate error to caller for proper error handling
        raise e

def save_courses(courses):
    """
    Save the given list of courses back to the JSON file.
    """
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(courses, f, indent=2)
    except Exception as e:
        # Re-raise so the caller can respond with a 500 error
        raise e

def next_id(courses):
    """
    Compute the next auto-incremented ID for a new course.
    Starts at 1 if the list is empty.
    """
    if not courses:
        return 1
    max_id = max((course.get('id', 0) for course in courses))
    return max_id + 1

def compute_course_stats(courses):
    """
    Compute course statistics: total count and counts by status.
    """
    by_status = {status: 0 for status in sorted(ALLOWED_STATUSES)}
    for course in courses:
        status = course.get("status")
        if status in ALLOWED_STATUSES:
            by_status[status] += 1
    return {"total": len(courses), "by_status": by_status}

def validate_date(date_str):
    """
    Validate that a date string is in YYYY-MM-DD format.
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except Exception:
        return False

def validate_course_fields(data, require_all=False):
    """
    Validate course fields coming from client.
    - If require_all is True, require name, description, target_date, and status.
    - Always validate fields that are present.
    Returns a list of error messages (empty if valid).
    """
    errors = []

    if require_all:
        required_fields = ["name", "description", "target_date", "status"]
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing field: {field}")

    if "name" in data:
        if not isinstance(data["name"], str) or not data["name"].strip():
            errors.append("Field 'name' must be a non-empty string.")

    if "description" in data:
        if not isinstance(data["description"], str):
            errors.append("Field 'description' must be a string.")

    if "target_date" in data:
        if not isinstance(data["target_date"], str) or not validate_date(data["target_date"]):
            errors.append("Field 'target_date' must be in YYYY-MM-DD format.")

    if "status" in data:
        if data["status"] not in ALLOWED_STATUSES:
            errors.append(
                f"Field 'status' must be one of: {', '.join(sorted(ALLOWED_STATUSES))}"
            )

    return errors

# ----------------------------
# Flask app and routes
# ----------------------------

app = Flask(__name__)

@app.route('/api/courses', methods=['POST'])
def create_course():
    """
    Create a new course.
    Required JSON fields: name, description, target_date (YYYY-MM-DD), status
    Auto-generates id and created_at.
    """
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "Missing or invalid JSON body."}), 400

    errors = validate_course_fields(payload, require_all=True)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        courses = load_courses()
    except Exception:
        return jsonify({"error": "Failed to read courses data."}), 500

    new_id = next_id(courses)
    created_at = datetime.utcnow().isoformat() + "Z"

    course = {
        "id": new_id,
        "name": payload["name"],
        "description": payload["description"],
        "target_date": payload["target_date"],
        "status": payload["status"],
        "created_at": created_at
    }

    courses.append(course)

    try:
        save_courses(courses)
    except Exception:
        return jsonify({"error": "Failed to write courses data."}), 500

    return jsonify(course), 201

@app.route('/api/courses', methods=['GET'])
def get_all_courses():
    """
    Get all courses.
    Returns a list of course objects.
    """
    try:
        courses = load_courses()
    except Exception:
        return jsonify({"error": "Failed to read courses data."}), 500

    return jsonify(courses), 200

@app.route('/api/courses/stats', methods=['GET'])
def get_course_stats():
    """
    Get course statistics: total count and counts by status.
    """
    try:
        courses = load_courses()
    except Exception:
        return jsonify({"error": "Failed to read courses data."}), 500

    return jsonify(compute_course_stats(courses)), 200

@app.route('/api/courses/<int:course_id>', methods=['GET'])
def get_course_by_id(course_id):
    """
    Get a specific course by id: /api/courses/1
    """
    try:
        courses = load_courses()
    except Exception:
        return jsonify({"error": "Failed to read courses data."}), 500

    course = next((c for c in courses if c.get('id') == course_id), None)
    if course is None:
        return jsonify({"error": "Course not found."}), 404

    return jsonify(course), 200

@app.route('/api/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    """
    Update an existing course (partial or full update in one call).
    Example: PUT /api/courses/1 with body { "status": "In Progress" }
    """
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "Missing or invalid JSON body."}), 400

    # Validate provided fields (optional fields allowed)
    errors = validate_course_fields(payload, require_all=False)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        courses = load_courses()
    except Exception:
        return jsonify({"error": "Failed to read courses data."}), 500

    idx = next((i for i, c in enumerate(courses) if c.get('id') == course_id), None)
    if idx is None:
        return jsonify({"error": "Course not found."}), 404

    updated = dict(courses[idx])

    # Apply updates for allowed fields if present
    for key in ["name", "description", "target_date", "status"]:
        if key in payload:
            updated[key] = payload[key]

    courses[idx] = updated

    try:
        save_courses(courses)
    except Exception:
        return jsonify({"error": "Failed to write courses data."}), 500

    return jsonify(updated), 200

@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    """
    Delete a course.
    Example: DELETE /api/courses/1
    """
    try:
        courses = load_courses()
    except Exception:
        return jsonify({"error": "Failed to read courses data."}), 500

    idx = next((i for i, c in enumerate(courses) if c.get('id') == course_id), None)
    if idx is None:
        return jsonify({"error": "Course not found."}), 404

    deleted = courses.pop(idx)

    try:
        save_courses(courses)
    except Exception:
        return jsonify({"error": "Failed to write courses data."}), 500

    return jsonify({"deleted": deleted}), 200

# ----------------------------
# Run the app
# ----------------------------

if __name__ == '__main__':
    # The server will run on http://127.0.0.1:5000 by default
    app.run(debug=True)