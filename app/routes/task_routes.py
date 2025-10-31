from flask import abort, Blueprint, make_response, request
from app.models.task import Task
from ..db import db
from app.routes.route_utilities import validate_model

bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')

@bp.get('')
def get_all_tasks():
    query = db.select(Task)
    tasks = db.session.scalars(query)

    task_list = []
    for task in tasks:
        task_list.append(task.to_dict())
    
    return task_list

@bp.get('/<task_id>')
def get_one_task_by_id(task_id):
    pass

@bp.post('')
def create_task():
    pass

@bp.put('/<task_id>')
def update_task(task_id):
    pass

@bp.delete('/<task_id>')
def delete_task(task_id):
    pass