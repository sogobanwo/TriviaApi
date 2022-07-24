import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category
from sqlalchemy.sql.functions import func


QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    present_questions = questions[start:end]
    return present_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def fetch_categories():
        categories = Category.query.all()
        
        if categories is None:
            abort(404)
            
        return jsonify({
            'success': True,
            'total_categories': len(categories),
            'categories': {category.id: category.type for category in categories}
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def fetch_questions():
        selection = Question.query.all()
        paginated_questions = paginate_questions(request, selection)
        categories = Category.query.all()


        if len(paginated_questions) == 0:
            abort(404)
        
        return jsonify({
            'success': True,
            'questions': paginated_questions,
            'total_questions': len(selection),
            'categories': {category.id: category.type for category in categories},
        }), 200
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        question = Question.query.filter(Question.id == id).one_or_none()
        if (question is None):
            abort(404)
        else:
            question.delete()
        return jsonify(), 204
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_new_question():
        body = request.get_json()

        try:
            new_question = body.get('question', None)
            new_answer = body.get('answer', None)
            new_category = body.get('category', None)
            new_difficulty = body.get('difficulty', None)
            int_difficulty = int(new_difficulty)

            question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=int_difficulty)
            question.insert()

            return jsonify({
                'success': True,
                'question_id': question.id,
            })

        except:
            abort(422)
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST']) 
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm')
        questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        paginated_questions = paginate_questions(request, questions)

        if len(paginated_questions) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'questions': paginated_questions,
            'total_questions': len(questions),
            'categories': {category.id: category.type for category in Category.query.all()}
            }), 200

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        get_categories = Category.query.get(category_id)
        questions = Question.query.join(Category, Category.id == Question.category).filter(Category.id == category_id).all()
        paginated_questions = paginate_questions(request, questions)
        
        if len(paginated_questions) < 1:
            abort(404)

        return jsonify({
            'success': True,
            'questions': paginated_questions,
            'total_questions': len(questions),
            'current_category': category_id
            }), 200
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        body = request.get_json()
       
        previous_questions = body.get('previous_questions', None)
        category = body.get('quiz_category', None)

        category_id = category.get('id')

        if (previous_questions is None or category is None):
            abort(400)
        
        try:
            order_by = func.random()
            if category_id == 0 :
                question = Question.query.order_by(order_by).filter(Question.id.notin_(previous_questions)).first()
            else:
                question = Question.query.filter(Question.category == category_id).order_by(order_by).filter(Question.id.notin_(previous_questions)).first()

            if question is None:
                return jsonify({
                    'success': True
            })

            return jsonify({
                'success': True,
                'question': question.format()
            })
        except Exception as e:
            print(e)
            abort(400)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

        
    return app

