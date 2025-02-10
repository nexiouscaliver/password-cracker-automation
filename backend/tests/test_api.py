import sys
import os
import json
import pytest

# Add the parent folder of tests to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app

# Patch the Celery task to avoid connecting to Redis.
@pytest.fixture(autouse=True)
def disable_celery(monkeypatch):
    # Import the task used in your route.
    from tasks.celery_tasks import crack_password_task
    class DummyTask:
        id = "dummy_task_id"
    # Patch apply_async so that when it's called, it returns a DummyTask.
    monkeypatch.setattr(crack_password_task, 'apply_async', lambda args, **kwargs: DummyTask())


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    # Configure Celery to run tasks eagerly during testing.
    app.config['CELERY_TASK_ALWAYS_EAGER'] = True
    app.config['CELERY_TASK_EAGER_PROPAGATES'] = True
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