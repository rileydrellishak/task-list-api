def test_get_tasks_sorted_by_id_asc(client, three_tasks):
    response = client.get('/tasks?sort=asc&sort_by=id')
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]['id'] == 1
    assert response_body[1]['id'] == 2
    assert response_body[2]['id'] == 3

def test_get_tasks_sorted_by_id_desc(client, three_tasks):
    response = client.get('/tasks?sort=desc&sort_by=id')
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]['id'] == 3
    assert response_body[1]['id'] == 2
    assert response_body[2]['id'] == 1

def test_get_tasks_sort_by_default(client, three_tasks):
    response = client.get('/tasks')
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]['title'] == 'Answer forgotten email 📧'
    assert response_body[1]['title'] == 'Pay my outstanding tickets 😭'
    assert response_body[2]['title'] == 'Water the garden 🌷'

def test_get_goals_sorted_by_id_asc(client, three_goals):
    response = client.get('/goals?sort=asc&sort_by=id')
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]['id'] == 1
    assert response_body[1]['id'] == 2
    assert response_body[2]['id'] == 3

def test_get_goals_sorted_by_id_desc(client, three_goals):
    response = client.get('/goals?sort=desc&sort_by=id')
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]['id'] == 3
    assert response_body[1]['id'] == 2
    assert response_body[2]['id'] == 1

def test_get_goals_sorted_by_title_asc(client, three_goals):
    response = client.get('/goals?sort=asc&sort_by=title')
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]['title'] == 'Perfect My Wind Down Routine 🌙'
    assert response_body[1]['title'] == 'Prioritize Self Care 🧖‍♀️'
    assert response_body[2]['title'] == 'Tidy Spaces, Tidy Mind 🫧'

def test_get_goals_sorted_by_title_desc(client, three_goals):
    response = client.get('/goals?sort=desc&sort_by=title')
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]['title'] == 'Tidy Spaces, Tidy Mind 🫧'
    assert response_body[1]['title'] == 'Prioritize Self Care 🧖‍♀️'
    assert response_body[2]['title'] == 'Perfect My Wind Down Routine 🌙'

def test_get_goals_sort_by_default(client, three_goals):
    response = client.get('/goals')
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]['title'] == 'Perfect My Wind Down Routine 🌙'
    assert response_body[1]['title'] == 'Prioritize Self Care 🧖‍♀️'
    assert response_body[2]['title'] == 'Tidy Spaces, Tidy Mind 🫧'

def test_get_goals_sorted_by_id_default_direction(client, three_goals):
    response = client.get('/goals?sort_by=id')
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]['id'] == 1
    assert response_body[1]['id'] == 2
    assert response_body[2]['id'] == 3