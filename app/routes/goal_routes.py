from flask import Blueprint, request, Response
from ..models.goal import Goal
from ..models.task import Task
from ..db import db
from .route_utilities import validate_model, create_model, get_models_with_filters, update_model

bp = Blueprint('goals_bp', __name__, url_prefix='/goals')

@bp.post('')
def create_goal():
    goal_data = request.get_json()
    return create_model(Goal, goal_data)

@bp.get('')
def get_all_goals():
    return get_models_with_filters(Goal, request.args)

@bp.get('/<goal_id>')
def get_goal_by_id(goal_id):
    goal = validate_model(Goal, goal_id)
    return goal.to_dict()

@bp.put('/<goal_id>')
def update_goal_title(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    return update_model(goal, request_body)

@bp.delete('<goal_id>')
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    return Response(status=204, mimetype='application/json')

@bp.post('/<goal_id>/tasks')
def post_task_ids_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.tasks = []

    for id in request_body['task_ids']:
        task = validate_model(Task, id)
        task.goal_id = goal.id
        
    db.session.commit()

    response = {
        'id': goal.id,
        'task_ids': [task.id for task in goal.tasks]
    }
    return response, 200

@bp.get('/<goal_id>/tasks')
def get_tasks_for_specific_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    response = goal.to_dict()
    response['tasks'] = [task.to_dict() for task in goal.tasks]
    return response, 200
