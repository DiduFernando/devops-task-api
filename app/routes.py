from flask import Blueprint, jsonify, request
from . import db
from .models import Task

api = Blueprint("api", __name__)

@api.get("/")
def home():
    return jsonify({
        "service": "DevOps Task API",
        "status": "running",
        "version": "1.0.0"
    })

@api.get("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@api.get("/tasks")
def get_tasks():
    tasks = Task.query.order_by(Task.id.asc()).all()
    return jsonify([task.to_dict() for task in tasks])

@api.post("/tasks")
def create_task():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    description = str(data.get("description", "")).strip()

    if not title:
        return jsonify({"error": "title is required"}), 400

    task = Task(title=title, description=description)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@api.put("/tasks/<int:task_id>")
def update_task(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        return jsonify({"error": "task not found"}), 404

    data = request.get_json(silent=True) or {}

    if "title" in data:
        title = str(data["title"]).strip()
        if not title:
            return jsonify({"error": "title cannot be empty"}), 400
        task.title = title

    if "description" in data:
        task.description = str(data["description"]).strip()

    if "completed" in data:
        task.completed = bool(data["completed"])

    db.session.commit()
    return jsonify(task.to_dict())

@api.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        return jsonify({"error": "task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "task deleted"})
