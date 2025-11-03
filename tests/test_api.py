import unittest
from backend.app import app

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_members(self):
        response = self.app.get('/api/members')
        self.assertEqual(response.status_code, 200)

    def test_create_member(self):
        response = self.app.post('/api/members', json={
            'name': 'John Doe',
            'email': 'john@example.com'
        })
        self.assertEqual(response.status_code, 201)

    def test_get_books(self):
        response = self.app.get('/api/books')
        self.assertEqual(response.status_code, 200)

    def test_create_book(self):
        response = self.app.post('/api/books', json={
            'title': 'The Great Gatsby',
            'author': 'F. Scott Fitzgerald'
        })
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()