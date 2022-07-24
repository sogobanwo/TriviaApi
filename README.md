# API Development and Documentation Final Project

## Trivia App
This Trivia App is invested in creating bonding experiences for employees and students. This can be used to hold trivia on a regular basis and play the game so they can start holding trivia and seeing who's the most knowledgeable of the bunch. 

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Getting Started

Install Dependencies
Dependencies for this project includes Pip, Python, Node.js and npm.

Frontend Dependencies
Navigate to the frontend directory and the install npm 

Example:
In the terminal run:
cd frontend
npm install

To start the frontend:
npm start to start the frontend 

Backend Dependencies

Set up your virtual environment and navigate to the backend directory and run the following command:

cd backend

To intall requirements:
pip install -r requirements.txt
 
To populate the database at backend:
psql trivia < trivia.psql

To start the Flask server at the backend:
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run

API Reference:

Errors will be displayed in the following JSON format:

{
    "error": 404,
    "message": "resource not found",
    "success": false
}

The 5 types of API errors that will be returned:

400: bad request.
404: resource not found.
405: method not allowed.
422: unprocessable.
500: internal server error.

The Various Endpoints:

GET '/categories'
This endpoint fetches a dictionary of categories in which eaach key is the ids and the value is the corresponding string of the category
Example curl http://127.0.0.1:5000/categories

{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
}

GET '/questions'
This endpoint fetches all the questions in the database with a pagination of 10 questions per page.
Example curl http://127.0.0.1:5000/questions

{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        }
    ],
    "success": true,
    "total_questions": 18
}

GET '/categories/int:id/questions'
This endpoint gets questions by category id using url parameters and returns a JSON object. It also returns the total number of questions in the category.
Example curl http://127.0.0.1:5000/categories/1/questions
{
  "current_category": 1, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "success": true, 
  "total_questions": 3
}
DELETE '/questions/int:id'
This endpoint deletes a question with the matching id, it also returns the ID of the question that was deleted upon successful deletion.
Example curl -X DELETE http://127.0.0.1:5000/questions/1
{
    "deleted": 1,
    "success": true
}

POST '/questions'
This endpoint creates a new question and returns the ID of the question that was created upon successful creation.
Example curl -X POST -H "Content-Type: application/json" -d '{"question": "What is my name?", "answer": "Banwo Olorunsogo", "category": "4", "difficulty": "3"}' http://127.0.0.1:5000/questions
{
    "created": 25,
    "success": true
}

POST '/questions/search'
This endpoint searches for questions based on the search term and returns a JSON object.
Example curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "autobiography"}' http://127.0.0.1:5000/questions/search
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
  ],
  "success": true,
  "total_questions": 1
}
POST '/quizzes'
This endpoint creates a new quiz and returns the ID of the quiz that was created upon successful creation.
Example: curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [7, 8], "quiz_category": {"type": "Geography", "id": "3"}} http://127.0.0.1:5000/quizzes

  "question": {
    "answer": "Agra", 
    "category": 3, 
    "difficulty": 2, 
    "id": 15, 
    "question": "The Taj Mahal is located in which Indian city?"
  }, 
  "success": true
}

Author and Acknowledgements
The API (__init__.py), test suite (test_flaskr.py), and this README.md was aurthored by BANWO OLORUNSOGO. All other project files, including the models, backend and frontend, were created by Udacity as a project template for the Full Stack Web Developer Nanodegree program.