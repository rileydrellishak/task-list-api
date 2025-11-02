from flask import abort, Blueprint, make_response, request, Response
from app.models.goal import Goal
from ..db import db
from app.routes.route_utilities import validate_model
from datetime import datetime
import os
import requests

bp = Blueprint('goals_bp', __name__, url_prefix='/goals')

@bp.get('/<goal_id>')
def get_one_task_by_id(goal_id):
    goal = validate_model(Goal, goal_id)
    return goal.to_dict()