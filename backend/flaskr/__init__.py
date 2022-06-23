import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
     # Implement pagination
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    # CORS(app)


    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
            )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        # Query categories
        categories = Category.query.all()
        # Handle error if no result is found
        if categories is None:
            abort(404)
        # List categories in a paginated manner   
        categories_list = paginate_questions(request, categories)
        # Initialize categories dictionary
        categories_dictionary = {}

        for i in categories_list:
            # Assign id in category list to that in category dictionary
            # categories_dictionary will then be a dictionary that has a list of dictionaries
           categories_dictionary[i['id']] = i['type']
                
        return jsonify({
            'success': True,
            'categories' : categories_dictionary
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


    @app.route('/questions')
    def get_questions():
       
       selection = Question.query.order_by(Question.id).all() # Get all questions
       categories = Category.query.all() # Get all categories
       categories_list = paginate_questions(request, categories)
       questions_list = paginate_questions(request, selection)

       current_category_list ={}
       categories_dictionary = {}


       for i in categories_list:
           categories_dictionary[i['id']] = i['type']
           
       if len(questions_list) == 0:
           abort(404)

       return jsonify({
           'success': True,
            'questions': questions_list,
            'categories': categories_dictionary,
            'total_questions':len(selection)
            })
            


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        # Get questions and filter them according to question id
       question = Question.query.filter(Question.id == question_id).one_or_none()
       # If there are go questions gotten, return error
       if question is None:
           abort(404)
       # Delete the question   
       try:
           question.delete()
           return jsonify({
               'success' : True,
               'deleted' : question_id,
                "total_questions": len(Question.query.all()),
               })
       # Display an error if unable to delete from database      
       except:
           abort(422)



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
    def create_questions():
        # Get the json body of the request
        body = request.get_json()
        # Check if body contains some required parameters before proceeding
        if (body.__contains__('question')) and (body.__contains__('answer')) and (body.__contains__('category')) and (body.__contains__('difficulty')):
            
            # Get the values of each parameters
            new_question = body.get("question")
            new_answer = body.get("answer")
            new_category = body.get("category")
            new_difficulty = body.get("difficulty")

            # Return error if the values are empty
            if (new_question == ''):
                abort(400)

            if (new_answer == ''):
                abort(400)

            if (new_category == ''):
                abort(400)

            if (new_difficulty == ''):
                abort(400)

            # Insert the values into the database
            try:
                question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
                question.insert()
                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)
                
                return jsonify({
                    "success": True,
                    "created": question.id,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all()),
                    })
            # If there is an error during insertion into database, return an error
            except:
                abort(422)
        # If body doesnt contain required parameters, return error
        else:
            abort(400)
  


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
        # Get json body from the user's request
        body = request.get_json()

        # Check if the request has the key, "searchTerm" then get it
        if (body.__contains__('searchTerm')):
            search = body.get('searchTerm')
            # If searchTerm id empty, return an error
            if (search == ''):
                abort(400)
            # Query the database
            try:
                if search:
                    selections = Question.query.order_by(Question.id).filter(
                        Question.question.ilike("%{}%".format(search)))
             
                    current_question = paginate_questions(request, selections)

                    return jsonify({
                        "success": True,
                        "questions": current_question,
                        "total_questions": len(selections.all()),
                        })
            # Return error, if database query fails
            except:
                abort(422)
        # If request doesn't have a searchTerm, return an error
        else:
            abort(400)



    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_based_on_category(category_id):

        # Query for all questions according to category id
     
        selection = (Question.query.filter(Question.category == category_id).order_by(Question.id).all())
        if selection is None:
            abort(404)

        # Paginate and format question into list of dictionary
        questions = paginate_questions(request, selection)

        # If question is empty return an error
        if questions == []:
            abort(404)

        # Return this if succesfull
        return jsonify({
        'success': True,
        'questions': questions,
        'total_questions': len(selection),
        'current_category' : category_id
        })
    

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
    def play_quizzes():
        body = request.get_json()

        # If body doesn't contain a JSON object, return error
        if not body:
            abort(400)
        
        # Get paramters from JSON Body.
        previous_questions = body.get('previous_question', None)
        quiz_category = body.get('quiz_category', None)

        # If previous_questions is specified
        if previous_questions:
            # If current category has a value/is specified and its value is not 0
            if quiz_category and quiz_category['id']!=0:

                # Query for questions in that category except the previous question
                question_list = (Question.query
                .filter(Question.category == str(quiz_category['id']))
                .filter(Question.id.notin_(previous_questions))
                .all())
            else:
                # if the current category is not specified, 
                # Query for all the questions in database except the previous question
                question_list = (Question.query
                .filter(Question.id.notin_(previous_questions))
                .all())
                
        else:
            # If previous question isn't specified
            # If current category has a value/is specified and its value is not 0
            if quiz_category and quiz_category['id']!=0:
                # Query for questions in that category
                question_list = (Question.query
                .filter(Question.category == str(quiz_category['id']))
                .all())
            else:
                # If previous question isn't specified
                # If current category is not specified
                # Get all questions from the database
                question_list = (Question.query.all())
            
        
        # Format questions & get a random question
        questions_formatted = paginate_questions(request, question_list)
        random_question = questions_formatted[random.randint(0, len(questions_formatted)-1)]
        
        return jsonify({
            'success': True,
            'question': random_question
        })



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
            "message": "Not found"
            }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, 
            "error": 422, 
            "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    return app
