import unittest
from app import app, db, Task  # Adjust imports based on your actual file structure

class TaskManagementAppTestCase(unittest.TestCase):
    def setUp(self):
        # Set up a test client
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

    def test_add_task(self):
        # Test adding a task
        response = self.app.post('/add', data=dict(title='Test Task', description='Test Description', due_date='2023-10-10'))
        self.assertEqual(response.status_code, 302)  # Redirect after adding a task

    def test_task_creation(self):
        # Test the creation of a task object
        task = Task(title='Test Task', description='Test Description', due_date='2023-10-10')
        db.session.add(task)
        db.session.commit()
        self.assertEqual(Task.query.count(), 1)

    def test_task_deletion(self):
        # Test deleting a task
        task = Task(title='Test Task', description='Test Description', due_date='2023-10-10')
        db.session.add(task)
        db.session.commit()
        task_id = task.id
        response = self.app.get(f'/delete/{task_id}')
        self.assertEqual(response.status_code, 302)  # Redirect after deleting a task
        self.assertEqual(Task.query.count(), 0)

    def test_task_completion(self):
        # Test marking a task as complete
        task = Task(title='Test Task', description='Test Description', due_date='2023-10-10')
        db.session.add(task)
        db.session.commit()
        task_id = task.id
        response = self.app.get(f'/complete/{task_id}')
        self.assertEqual(response.status_code, 302)  # Redirect after completing a task
        task = Task.query.get(task_id)
        self.assertTrue(task.completed)

    def test_due_date_validation(self):
        # Test due date validation
        response = self.app.post('/add', data=dict(title='Test Task', description='Test Description', due_date='2022-01-01'))
        self.assertIn(b'Invalid due date', response.data)  # Assuming the app returns an error message for past due dates

if __name__ == '__main__':
    unittest.main()
