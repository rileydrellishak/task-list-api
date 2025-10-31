from flask import Blueprint

bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')

@bp.get('')
def get_all_tasks():
    pass

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