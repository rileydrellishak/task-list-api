from flask import Blueprint, request, Response
from app.models.goal import Goal
from app.models.task import Task
from ..db import db
from app.routes.route_utilities import validate_model, create_model

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
    return create_model(Goal, request_body)

@bp.patch('/<goal_id>')
def update_goal_title(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    
    goal.title = request_body['title']

    db.session.commit()

    return Response(status=204, mimetype='application/json')

@bp.delete('/<goal_id>')
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype='application/json')

@bp.post('/<goal_id>/tasks')
def send_list_of_task_ids_to_goal(goal_id):
    request_body = request.get_json()
    goal = validate_model(Goal, goal_id)

    goal.tasks = []

    for task_id in request_body['task_ids']:
        task = validate_model(Task, task_id)
        task.goal_id = goal_id
    
    db.session.commit()

    request_body['id'] = goal.id

    return request_body, 200

@bp.get('/<goal_id>/tasks')
def get_tasks_from_goal_id(goal_id):
    goal = validate_model(Goal, goal_id)

    query = db.select(Task).where(Task.goal_id == goal_id)
    tasks = db.session.scalars(query)

    response = goal.to_dict()
    response['tasks'] = []

    for task in tasks:
        task_dict = task.to_dict()
        task_dict['goal_id'] = goal.id
        response['tasks'].append(task_dict)

    return response