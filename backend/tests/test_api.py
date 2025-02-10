# tests/test_api.py
import json
import pytest
import sys
import os
# Add the parent folder of tests to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_submit_hash_no_data(client):
    response = client.post('/api/submit', data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400

def test_submit_hash_with_data(client):
    # MD5 hash for 'password'
    test_hash = '5f4dcc3b5aa765d61d8327deb882cf99'
    data = {
        'hash': test_hash,
        'hash_algorithm': 'md5',
        'method': 'rainbow_table'
    }
    response = client.post('/api/submit', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 202
    json_data = response.get_json()
    assert 'task_id' in json_data
