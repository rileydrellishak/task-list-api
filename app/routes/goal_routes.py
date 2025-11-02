from flask import abort, Blueprint, make_response, request, Response
from app.models.goal import Goal
from ..db import db
from app.routes.route_utilities import validate_model
from datetime import datetime
import os
import requests

bp = Blueprint('goals_bp', __name__, url_prefix='/goals')

@bp.get('')
def get_all_goals():
    query = db.select(Goal)
    goals = db.session.scalars(query)

    response = []
    for goal in goals:
        response.append(goal.to_dict())
    
    return response

@bp.get('/<goal_id>')
def get_one_goal_by_id(goal_id):
    goal = validate_model(Goal, goal_id)
    return goal.to_dict()

@bp.post('')
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal.from_dict(request_body)

    except KeyError as error: # Missing keys
        response = {'details': "Invalid data"}
        abort(make_response(response, 400))
    
    db.session.add(new_goal)
    db.session.commit()

    new_goal_dict = new_goal.to_dict()

    return new_goal_dict, 201

@bp.patch('/<goal_id>')
def mark_task_incomplete(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body['title']

    db.session.commit()

    response_body = goal.to_dict()

    return response_body, 201

@bp.delete('/<goal_id>')
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype='application/json')