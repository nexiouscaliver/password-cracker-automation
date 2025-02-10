# api/routes.py
from flask import request, jsonify
from flask_restful import Resource
from tasks.celery_tasks import crack_password_task

def initialize_routes(api):
    api.add_resource(SubmitHash, '/api/submit')
    api.add_resource(TaskStatus, '/api/status/<string:task_id>')
    api.add_resource(TaskResult, '/api/result/<string:task_id>')

class SubmitHash(Resource):
    def post(self):
        data = request.get_json(force=True)
        hash_value = data.get('hash')
        hash_algorithm = data.get('hash_algorithm', 'md5')
        method = data.get('method', 'dictionary')  # Options: 'brute_force', 'dictionary', 'rainbow'
        
        if not hash_value:
            return {'error': 'Hash value is required'}, 400

        # Start the cracking task asynchronously
        task = crack_password_task.apply_async(args=[hash_value, hash_algorithm, method])
        return {'task_id': task.id}, 202

class TaskStatus(Resource):
    def get(self, task_id):
        from celery.result import AsyncResult
        task_result = AsyncResult(task_id)
        if task_result.state == 'PENDING':
            response = {
                'state': task_result.state,
                'status': 'Task pending...'
            }
        elif task_result.state != 'FAILURE':
            response = {
                'state': task_result.state,
                'status': task_result.info.get('status', ''),
                'current': task_result.info.get('current', 0),
                'total': task_result.info.get('total', 1)
            }
        else:
            # Something went wrong in the background job
            response = {
                'state': task_result.state,
                'status': str(task_result.info),
            }
        return response, 200

class TaskResult(Resource):
    def get(self, task_id):
        from celery.result import AsyncResult
        task_result = AsyncResult(task_id)
        if task_result.state == 'SUCCESS':
            return {'result': task_result.result.get('result')}, 200
        else:
            return {'error': 'Task not completed yet'}, 202
