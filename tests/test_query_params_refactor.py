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

def test_get_goals_sorted_by_id_asc(client, )