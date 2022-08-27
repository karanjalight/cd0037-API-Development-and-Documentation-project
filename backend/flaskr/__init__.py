from crypt import methods
import os
from sre_constants import SUCCESS
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import desc

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_books(request, questions):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    books = [question.format() for question in questions]
    current_books = books[start:end]

    return current_books

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers 
    # =1=====-----backend is set up --------------------------
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
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
     @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    #=================DONE==================

  


    @app.route('/v1/categories', methods=['GET'])
    def category():
        categories = Category.query.all()
        
        category = [category.format() for category in categories]
        
        print(category)
        

        return jsonify({
            'success': True,
            'category' : category,
            
                                  
        
        })


    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
#=================================DONE=================================


# controller function for handling getting questions from category.

    @app.route('/v1/categories/<int:category_id>/questions', methods=['GET'])
    def question(category_id):

        categories = Category.query.filter(Category.id==category_id)
        questions = Question.query.filter(Question.category==category_id).all()

        category = [category.format() for category in categories]
        current_books = paginate_books(request, questions)
        print(category_id)
        print(category)
       
                

        return jsonify({
            'success': True,
            'questions' : current_books,
            'category' : category,
            
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

    #========================DONE=====================================================

    @app.route('/v1/questions/<int:question_id>', methods=['GET'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id== question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            questions = Question.query.order_by(Question.id).all()
            current_books = paginate_books(request, questions)

            print(question)
            print(len(Question.query.all()))
            print('deleted!')
            
            return jsonify({
                'success': True,
                'deleted' : question_id,   
                'questions' : current_books,
                'total_questions' : len(Question.query.all())
                })
        except:
            print('aborted')
            abort(422)


   # TEST: When you click the trash icon next to a question, the question will be removed.
    #This removal will persist in the database and when you refresh the page.
    
            

#============================DONE======================@TODO:
#Create an endpoint to DELETE question using a question ID.====================




    @app.route('/v1/new-question', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        try:
            question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
            question.insert()

            questions = Question.query.order_by(Question.id).all()
            current_books = paginate_books(request, questions)

            return jsonify({
            'success': True,
            'created': question.id,
            'questions': current_books,
            'total_questions': len(Question.query.all())

            }) 


        except:
            print("error posting!")
            abort(422)

    

    @app.route('/v1/questions', methods=['POST'])
    def search_question():
 
        body = request.get_json()

        #getting the value of the searched parameter
        search_questions = body.get('question', None)
        question = f'{search_questions}'
        
        question_search = Question.query.filter(Question.question.ilike('%what%')).order_by(Question.id).all()
        print(question_search)

        current_question = paginate_books(request, question_search)
        print(current_question)

       
        return jsonify({
            'success': True,
            'name':  question ,
            'searched-question': current_question,
            'number_of_questions': len(Question.query.filter(Question.question.ilike("%what%")).order_by(Question.id).all()
        )

            

        })
        
       

               

    return app
       

  
