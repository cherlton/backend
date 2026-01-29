from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.agents.supervisor import SupervisorAgent

skills_bp = Blueprint("skills", __name__)

@skills_bp.route("/", methods=["POST"])
@jwt_required()
def build_skill_path():
    data = request.get_json()
    skill = data.get("skill")
    user_id = get_jwt_identity()

    supervisor = SupervisorAgent()
    result = supervisor.handle_skill_request(
        skill=skill,
        user_id=user_id
    )

    return jsonify(result), 200

