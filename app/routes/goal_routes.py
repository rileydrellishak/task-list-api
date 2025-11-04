from flask import Blueprint, request, Response
from ..models.goal import Goal
from ..db import db
from .route_utilities import validate_model, create_model

bp = Blueprint('goals_bp', __name__, url_prefix='/goals')

@bp.get('')
def get_all_goals():
    query = db.select(Goal)
    goals = db.session.scalars(query)
    return [goal.to_dict() for goal in goals]

@bp.post('')
def create_goal():
    goal_data = request.get_json()
    return create_model(Goal, goal_data)

@bp.delete('<goal_id>')
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    return Response(status=204, mimetype='application/json')