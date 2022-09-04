import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}@{}/{}".format('postgres:lavie','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
        self.good_question = {
            "question": "Guinea is a country from wich continent",
            "answer" : "Africa",
            "category" : 3,
            "difficulty": 3
        }
        
        self.bad_question = {
             "question": "",
             "answer": "",
              "category": 10,
              "difficulty": 10
        }
    def tearDown(self):
        """Executed after reach test"""
        pass

   
    def test_retrieve_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
    
    def test_fail_retrieve_categories(self):
        res = self.client().get('/categories/')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")
    
    def test_retrieve_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        
    def test_fail_retrieve_questions(self):
        res = self.client().get('/questions?page=50')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")
    
    def test_delete_question(self):
        res = self.client().delete('/questions/17') 
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 17)
    
    def test_fail_delete_question(self):
        res = self.client().delete('/questions/80')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")
    
    def test_create_question(self):
        res = self.client().post('/questions', json=self.good_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_cod, 200)
        self.assertEqual(data['success'], True)
    
    def test_fail_create_question(self):
        res = self.client().post('/questions', json=self.bad_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")
        
    def test_questions_by_category(self):
        res = self.client().post('/categories/1/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        
    def test_fail_questions_by_category(self):
        res = self.client().post('/categories/10/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")
        
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()