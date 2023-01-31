from flask import jsonify
import re

def validate_password_strength(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search("[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search("[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search("[0-9]", password):
        return False, "Password must contain at least one digit"
    if not re.search("[!@#$%^&*()_+=-]", password):
        return False, "Password must contain at least one special character (!@#$%^&*()_+=-)"
    return True, "Password is strong"

def validateLoginData( username, password):
    if not username:
        return jsonify({"error": "Username is required"}), 400
    if not password:
        return jsonify({"error": "Password is required"}), 400

def validateEmployeeData(name, skills,designation_id,proj_id):
    if not name:
        return jsonify({"error": "name is required"}), 400
    if not skills:
        return jsonify({"error": "skills is required"}), 400
    if not designation_id:
        return jsonify({"error": "designation_id is required"}), 400
    if not proj_id:
        return jsonify({"error": "proj_id is required"}), 400

def validateProjectData(name, vertical,start_date,department,status):
    if not name:
        return jsonify({"error": "name is required"}), 400
    if not vertical:
        return jsonify({"error": "vertical is required"}), 400
    if not start_date:
        return jsonify({"error": "start_date is required"}), 400
    if not department:
        return jsonify({"error": "department is required"}), 400 
    if not status:
        return jsonify({"error": "status is required"}), 400       