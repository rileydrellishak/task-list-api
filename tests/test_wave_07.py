import pytest
from werkzeug.exceptions import HTTPException
from app.models.goal import Goal
from app.models.task import Task
from app.routes.route_utilities import create_model, validate_model

def test_route_utilities_validate_model_with_task(client, three_tasks):
    task_1 = validate_model(Task, 1)
    task_2 = validate_model(Task, 2)
    task_3 = validate_model(Task, 3)

    assert task_1.id == 1
    assert task_1.title == "Water the garden 🌷"
    assert task_1.description == ""
    assert task_1.completed_at is None

    assert task_2.id == 2
    assert task_2.title == "Answer forgotten email 📧"

    assert task_3.id == 3
    assert task_3.title == "Pay my outstanding tickets 😭"

def test_route_utilities_validate_model_with_task_invalid_id(client, three_tasks):
    with pytest.raises(HTTPException) as e:
        result_task = validate_model(Task, "One")
    
    response = e.value.get_response()
    assert response.status_code == 400
    assert response.get_json() == {"message": "Task One invalid"}

def test_route_utilities_validate_model_with_task_missing_id(client, three_tasks):
    with pytest.raises(HTTPException) as e:
        result_task = validate_model(Task, 4)
    
    response = e.value.get_response()
    assert response.status_code == 404
    assert response.get_json() == {'message': 'Task 4 not found'}

def test_route_utilities_validate_model_with_goal(client, one_goal):
    goal_1 = validate_model(Goal, 1)

    assert goal_1.id == 1
    assert goal_1.title == "Build a habit of going outside daily"

def test_route_utilities_validate_model_with_goal_invalid_id(client, one_goal):
    with pytest.raises(HTTPException) as e:
        result_task = validate_model(Goal, "One")
    
    response = e.value.get_response()
    assert response.status_code == 400
    assert response.get_json() == {"message": "Goal One invalid"}

def test_route_utilities_validate_model_with_goal_missing_id(client, one_goal):
    with pytest.raises(HTTPException) as e:
        result_task = validate_model(Goal, 4)
    
    response = e.value.get_response()
    assert response.status_code == 404
    assert response.get_json() == {'message': 'Goal 4 not found'}

def test_route_utilities_create_model_with_task(client):
    request_body = {
        "title": "Make the bed",
        "description": "",
        "completed_at": None
    }
    
    response = create_model(Task, request_body)

    assert response[0]["id"] == 1
    assert response[0]["title"] == "Make the bed"
    assert response[0]["description"] == ""
    assert response[0]["is_complete"] == False
    assert response[1] == 201

def test_route_utilities_create_model_with_task_missing_title(client):
    request_body = {
        "description": "",
        "completed_at": None
    }
    
    with pytest.raises(HTTPException) as e:
        create_model(Task, request_body)
    
    response = e.value.get_response()
    assert response.status_code == 400
    assert response.get_json() == {"details": "Invalid data"}

def test_route_utilities_create_model_with_goal(client):
    request_body = {
        "title": "Seize the Day!"
    }

    response = create_model(Goal, request_body)

    assert response[0]["id"] == 1
    assert response[0]["title"] == "Seize the Day!"
    assert response[1] == 201

def test_route_utilities_create_model_with_goal_missing_title(client):
    request_body = {
    }
    
    with pytest.raises(HTTPException) as e:
        create_model(Goal, request_body)
    
    response = e.value.get_response()
    assert response.status_code == 400
    assert response.get_json() == {"details": "Invalid data"}
