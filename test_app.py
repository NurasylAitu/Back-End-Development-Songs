import pytest
from app import app, items

@pytest.fixture
def client():
    items.clear()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    assert client.get('/health').status_code == 200

def test_count(client):
    assert client.get('/count').json['count'] == 0

def test_create_get_update_delete(client):
    created = client.post('/songs', json={'title': 'Example'})
    assert created.status_code == 201
    item_id = created.json['id']
    assert client.get('/songs/'+str(item_id)).json['title'] == 'Example'
    assert client.put('/songs/'+str(item_id), json={'title':'Updated'}).status_code == 200
    assert client.delete('/songs/'+str(item_id)).status_code == 204
    assert client.get('/songs/'+str(item_id)).status_code == 404
