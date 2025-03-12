import unittest
import json
from datetime import datetime
from app import app, db, Task

class TaskManagementAppTestCase(unittest.TestCase):
    def setUp(self):
        # Set up a test client
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        # Clean up after each test
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        # Test the home page
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_task(self):
        # Test creating a task
        task_data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'due_date': '2023-12-31'
        }
        response = self.app.post('/tasks', json=task_data)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['title'], 'Test Task')
        self.assertEqual(Task.query.count(), 1)

    def test_get_tasks(self):
        # Test getting tasks
        task = Task(title='Test Task', description='Test Description', due_date=datetime(2023, 12, 31).date())
        db.session.add(task)
        db.session.commit()
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'Test Task')

    def test_update_task(self):
        # Test updating a task
        task = Task(title='Test Task', description='Test Description', due_date=datetime(2023, 12, 31).date())
        db.session.add(task)
        db.session.commit()
        task_id = task.id
        update_data = {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'due_date': '2024-01-01'
        }
        response = self.app.put(f'/tasks/{task_id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['title'], 'Updated Task')

    def test_delete_task(self):
        # Test deleting a task
        task = Task(title='Test Task', description='Test Description', due_date=datetime(2023, 12, 31).date())
        db.session.add(task)
        db.session.commit()
        task_id = task.id
        response = self.app.delete(f'/tasks/{task_id}')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Task.query.count(), 0)

    def test_invalid_due_date(self):
         # Test invalid due date format
        task_data = {
            'title': 'Invalid Date Task',
            'description': 'Test Description',
            'due_date': '2023/12/31'  # Invalid format
        }
        response = self.app.post('/tasks', json=task_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn("Invalid date format", data['error'])

if __name__ == '__main__':
    unittest.main()
    
