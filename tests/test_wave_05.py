from app.models.goal import Goal
import pytest

def test_goal_to_dict():
    new_goal = Goal(id=1, title="Seize the Day!")
    
    goal_dict = new_goal.to_dict()

    assert goal_dict["id"] == 1
    assert goal_dict["title"] == "Seize the Day!"

def test_goal_to_dict_no_id():
    #Arrange
    new_goal = Goal(title="Seize the Day!")
    
    #Act
    goal_dict = new_goal.to_dict()

    #Assert
    assert goal_dict["id"] is None
    assert goal_dict["title"] == "Seize the Day!"

def test_goal_to_dict_no_title():
    #Arrange
    new_goal = Goal(id=1)
    
    #Act
    goal_dict = new_goal.to_dict()

    #Assert
    assert goal_dict["id"] == 1
    assert goal_dict["title"] is None

def test_goal_from_dict():
    goal_dict =  {
        "title": "Seize the Day!",
    }

    goal_obj =  Goal.from_dict(goal_dict)

    assert goal_obj.title == "Seize the Day!"

def test_goal_from_dict_no_title():
    goal_dict =  {
    }
    with pytest.raises(KeyError, match = 'title'):
        Goal.from_dict(goal_dict)

def test_get_goals_no_saved_goals(client):
    response = client.get("/goals")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_goals_one_saved_goal(client, one_goal):
    response = client.get("/goals")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "Build a habit of going outside daily"
        }
    ]

def test_get_goal(client, one_goal):
    response = client.get("/goals/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Build a habit of going outside daily"
    }

def test_get_goal_not_found(client):
    response = client.get("/goals/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert "message" in response_body
    assert response_body == {'message': 'Goal 1 not found'}
    
def test_create_goal(client):
    response = client.post("/goals", json={
        "title": "My New Goal"
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "title": "My New Goal"
    }

def test_update_goal(client, one_goal):
    response = client.put("/goals/1", json={
        "title": "My New Title"
    })

    assert response.status_code == 204
    
    # check that the goal was updated
    response = client.get('goals/1')
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body['title'] == 'My New Title'

def test_update_goal_not_found(client):
    response = client.delete("/goals/1")
    assert response.status_code == 404

    response_body = response.get_json()
    assert "message" in response_body
    assert response_body == {'message': 'Goal 1 not found'}

def test_delete_goal(client, one_goal):
    response = client.delete("/goals/1")
    assert response.status_code == 204

    # Check that the goal was deleted
    response = client.get("/goals/1")
    assert response.status_code == 404

    response_body = response.get_json()
    assert "message" in response_body
    assert response_body == {'message': 'Goal 1 not found'}

def test_delete_goal_not_found(client):
    response = client.delete("/goals/1")
    assert response.status_code == 404

    response_body = response.get_json()
    assert "message" in response_body
    assert response_body == {'message': 'Goal 1 not found'}

def test_create_goal_missing_title(client):
    response = client.post("/goals", json={})
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {
        "details": "Invalid data"
    }
