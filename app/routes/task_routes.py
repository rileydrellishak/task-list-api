from flask import abort, Blueprint, request, Response
from app.models.task import Task
from ..db import db
from app.routes.route_utilities import validate_model, create_model
from datetime import datetime
import os
import requests

bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')

@bp.get('')
def get_all_tasks():
    query = db.select(Task)

    sort_param = request.args.get('sort')
    if sort_param == 'asc' or sort_param is None:
        query = query.order_by(Task.title)
    elif sort_param == 'desc':
        query = query.order_by(Task.title.desc())

    tasks = db.session.scalars(query)
    task_list = []
    for task in tasks:
        task_list.append(task.to_dict())
    
    return task_list

@bp.get('/<task_id>')
def get_one_task_by_id(task_id):
    task = validate_model(Task, task_id)
    return task.to_dict()

@bp.post('')
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)

@bp.put('/<task_id>')
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body['title']
    task.description = request_body['description']
    db.session.commit()

    return Response(status=204, mimetype='application/json')

@bp.delete('/<task_id>')
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype='application/json')

@bp.patch('/<task_id>/mark_incomplete')
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None

    db.session.commit()

    return Response(status=204, mimetype='application/json')

@bp.patch('/<task_id>/mark_complete')
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now().date()

    db.session.commit()
    slack_token = os.environ["SLACK_BOT_TOKEN"]
    channel_and_message = {
	'channel': 'task-notifications',
	'text': f'Someone just completed the task {task.title}'
    }
    headers = {
        'Authorization': slack_token
    }
    requests.post('https://slack.com/api/chat.postMessage', data=channel_and_message, json=channel_and_message, headers=headers)

    return Response(status=204, mimetype='application/json')