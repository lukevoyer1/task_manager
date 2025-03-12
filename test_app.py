import unittest
from app import app, db, Task
from datetime import datetime
from contextlib import contextmanager

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        """Set up the test client and initialize the database."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up the database after each test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()  # Explicitly close the database connection

    def test_index_route(self):
        """Test the index route."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_tasks_empty(self):
        """Test getting tasks when the database is empty."""
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_create_task(self):
        """Test creating a new task."""
        task_data = {
            "title": "Test Task",
            "description": "This is a test task.",
            "due_date": "2023-12-31"
        }
        response = self.app.post('/tasks', json=task_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['title'], "Test Task")
        self.assertEqual(response.json['description'], "This is a test task.")
        self.assertEqual(response.json['due_date'], "2023-12-31")
        self.assertEqual(response.json['status'], "pending")

    def test_create_task_missing_title(self):
        """Test creating a task without a title."""
        task_data = {
            "description": "This is a test task.",
            "due_date": "2023-12-31"
        }
        response = self.app.post('/tasks', json=task_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], "Title is required.")

    def test_create_task_invalid_date(self):
        """Test creating a task with an invalid due date."""
        task_data = {
            "title": "Test Task",
            "description": "This is a test task.",
            "due_date": "invalid-date"
        }
        response = self.app.post('/tasks', json=task_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], "Invalid date format. Use 'YYYY-MM-DD'.")

    def test_update_task(self):
        """Test updating an existing task."""
        # Create a task first
        with app.app_context():
            task = Task(
                title="Test Task",
                description="This is a test task.",
                due_date=datetime.strptime("2023-12-31", "%Y-%m-%d").date()
            )
            db.session.add(task)
            db.session.commit()
            task_id = task.id

        # Update the task
        with app.app_context():
            response = self.app.put(f'/tasks/{task_id}', json={
                "title": "Updated Task",
                "description": "This is an updated task.",
                "status": "Complete"
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['title'], "Updated Task")
            self.assertEqual(response.json['description'], "This is an updated task.")
            self.assertEqual(response.json['status'], "Complete")

    def test_delete_task(self):
        """Test deleting an existing task."""
        # Create a task first
        with app.app_context():
            task = Task(
                title="Test Task",
                description="This is a test task.",
                due_date=datetime.strptime("2023-12-31", "%Y-%m-%d").date()
            )
            db.session.add(task)
            db.session.commit()
            task_id = task.id

        # Delete the task
        with app.app_context():
            response = self.app.delete(f'/tasks/{task_id}')
            self.assertEqual(response.status_code, 204)

        # Verify the task is deleted
        response = self.app.get('/tasks')
        self.assertEqual(response.json, [])

if __name__ == '__main__':
    unittest.main()
