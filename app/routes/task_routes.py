from flask import abort, Blueprint, make_response, request, Response
from app.models.task import Task
from ..db import db
from app.routes.route_utilities import validate_model
from sqlalchemy import desc, asc

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

    try:
        new_task = Task.from_dict(request_body)

    except KeyError as error: # Missing keys
        response = {'details': "Invalid data"}
        abort(make_response(response, 400))
    
    db.session.add(new_task)
    db.session.commit()

    new_task_dict = new_task.to_dict()

    return new_task_dict, 201

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