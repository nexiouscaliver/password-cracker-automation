# tasks/celery_tasks.py
import time
from celery_worker import celery
from services.password_cracker import crack_password

@celery.task(bind=True)
def crack_password_task(self, hash_value, hash_algorithm, method, extra_data=None):
    total_steps = 100  # Simulate progress steps
    for i in range(total_steps):
        time.sleep(0.05)  # Simulate work (in a real scenario, integrate progress updates within each technique)
        self.update_state(state='PROGRESS', meta={'current': i + 1, 'total': total_steps})
    result = crack_password(hash_value, algorithm=hash_algorithm, method=method, extra_data=extra_data)
    return {'status': 'Task completed', 'result': result}
