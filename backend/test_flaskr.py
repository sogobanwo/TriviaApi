import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from settings import DB_NAME, DB_USER, DB_PASSWORD
load_dotenv()
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_username = os.environ.get("database_username")
        self.database_password = os.environ.get("database_password")
        self.database_host = os.environ.get("database_host")  
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(self.database_username, self.database_password, self.database_host, self.database_name)
        setup_db(self.app, self.database_path)
        self.new_question = {
            'question': 'Which year did Nigeria got independent?',
            'answer': 1990,
            'category': 1,
            'difficulty': 5
        }
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["categories"])

    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])

    def test_404_for_unavailable_questions_pages(self):
        res = self.client().get("/questions?page=457")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_questions_by_categories(self):
        res = self.client().get("/categories/2/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])

    def test_delete_question(self):
        response = self.client().delete('/questions/15')
        self.assertEqual(response.status_code, 204)
        

    def test_404_if_question_does_not_exist_on_delete(self):
        
        res = self.client().delete('/questions/256')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_new_question(self):
        response = self.client().post('/questions', json=self.new_question)
        data = json.loads(response.data)
        self.assertTrue(response.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertTrue(data['question_id'])

    def test_add_question_without_required_input(self):

        question = {
         'question': 'who is Olorunsogo',
        }
    
        res = self.client().post('/questions', json=question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)  

    def test_get_question_search_with_results(self):
        res = self.client().post("/questions/search", json={"searchTerm": "cup"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])

    def test_search_questions_with_no_result(self):
        search_term = {
            'searchTerm': 'No result found',
        }
        response = self.client().post('/search', json=search_term)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_quiz_question_from_all_categories(self):
        res = self.client().post("/quizzes", json={
            "previous_questions": [10, 6, 17],
            'quiz_category': {
                'id': 0,
                'type': 'All'
            }
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["question"])

    def test_get_quiz_question_from_one_category(self):
        res = self.client().post("/quizzes", json={
            "previous_questions": [5, 9],
            'quiz_category': {
                'id': 4,
                'type': 'History'
            }
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["question"])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()