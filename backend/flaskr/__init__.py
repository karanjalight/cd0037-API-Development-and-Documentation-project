from crypt import methods
import os
from sre_constants import SUCCESS
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import desc

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def paginate_books(request, questions):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    books = [question.format() for question in questions]
    current_books = books[start:end]

    return current_books

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def generate_random_integers(selection):
    num = random.randint(0 , len(selection) - 1)
    return num

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={'/': {'origins': '*'}})

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

  

#===this one gets all categories in the  Play section
#1
    @app.route('/categories', methods=['GET'])
    def category():
        categories = Category.query.all()
        
        #category = [category.format() for category in categories]          ===this is how to serialize some data
        categories_query = Category.query.order_by(Category.id).all()
        
        print(categories_query)
        

        return jsonify({
            'success': True,
            #'category' : category,
            'categories':{category.id: category.type for category in categories_query},
            'total_categories': len(categories_query)
            
                                  
        
        })


    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
#=================================DONE=================================YES



# controller function for handling getting questions from category.

    """ @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def question(category_id):

        categories = Category.query.filter(Category.id==category_id)
        questions = Question.query.filter(Question.category==category_id).all()

        category = [category.format() for category in categories]
        current_books = paginate_books(request, questions)
        print(category_id)
        print(category)
        print(current_books)

        #categories_questions = db.session.query(Question).join(Category).all() 
        #print(categories_questions)      
                

        return jsonify({
            'success': True,
            'questions' : current_books,
            'category' : category,
            'total_questions': len(questions),
            
            }) """


#2
    @app.route('/categories/<int:category_id>/questions')
    def retrieve_category_questions(category_id):
        try:
            category = Category.query.filter(Category.id == category_id).one_or_none()
            print('new stuffs')
            if category is None:
                abort(404)

            category_questions= Question.query.order_by(Question.id).filter(Question.category == category_id).all()
            current_questions = paginate_questions(request, category_questions)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(category_questions),
                'current_category': category.type
            })
        except:
            abort(404)



#3

    #========================DONE=====================================================
#====This is a delete function for the questions
#--3. => DELETE QUESTIONS
    """ @app.route('/questions/<int:question_id>', methods=['GET'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id== question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            questions = Question.query.order_by(Question.id).all()
            current_question = paginate_books(request, questions)

            print(question)
            print(len(Question.query.all()))
            print('deleted!')
            
            return jsonify({
                'success': True,
                'deleted' : question_id,   
                'questions' : current_question,
                'total_questions' : len(Question.query.all())
                })
        except:
            print('aborted')
            abort(422) """


    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question=Question.query.filter(Question.id==question_id).one_or_none()
            if question is None:
                abort(404)
            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                "success": True,
                "deleted": question_id,
                "questions": current_questions,
                "total_questions": len(selection)
            })
        except:
            db.session.rollback()
            abort(404)
        finally:
            db.session.close()

   # TEST: When you click the trash icon next to a question, the question will be removed.
    #This removal will persist in the database and when you refresh the page.
    
            

#============================DONE======================@TODO:
#Create an endpoint to DELETE question using a question ID.====================



#=================DONE=======================================
#====In the (add) section this one adds questions to the DB
    @app.route('/questions', methods=['POST'])
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

    
    #this one is used to get all the questions in the home page
    #--DONE===
    @app.route("/questions", methods = ['GET'])
    def retrieve_questions():
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)
        categories = Category.query.order_by(Category.id).all()


        if len(current_questions) == 0:
            abort(404)

        return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": len(Question.query.all()),
                "current_category": categories[0].type,
                "categories": {category.id:category.type for category in categories}
            })

    #=================DONE=======================================


    

    

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        search = request.form.get('search_term')
        print(search)
 
        body = request.get_json()

        #getting the value of the searched parameter
        search_questions = body.get('question', None)
        question = f'{search_questions}'
        print(question)
        
        question_search = Question.query.filter(Question.question.ilike('%'+question+'%')).order_by(Question.id).all()
        print(question_search)

        current_question = paginate_books(request, question_search)
        print(current_question)

       
        return jsonify({
            'success': True,
            'name':  question ,
            'searched-question': current_question,
            'number_of_questions': len(Question.query.filter(Question.question.ilike('%'+question+'%')).order_by(Question.id).all()
        )

            

        })

    @app.route("/quizzes", methods=["POST"])
    def quizes_and_answer():
        body = request.get_json()
        quiz_category = body.get('quiz_category')
        previous_questions = body.get('previous_questions')
        random_question = None

        try:
            if quiz_category is None or quiz_category['id'] == 0:
                questions_selection = [question.format() for question in Question.query.all()]
            else:
                questions_selection = [question.format() for question in Question.query.filter(Question.category == quiz_category['id']).all()]
                        
            questions = []
            for question in questions_selection:
                if question['id'] not in previous_questions:
                    questions.append(question)
                
            if (len(questions) > 0):
                random_question = random.choice(questions)
                    
            return jsonify({
                'success': True,
                'question': random_question,
                'previous_questions': previous_questions
            })   
        except:
            abort(422)


    #ERROR HANDLERS========
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "Resource Not Found"}),
            404
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422)
    
    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify({"success": False, "error": 400, "message": "bad request"}), 400)

    @app.errorhandler(500)
    def bad_request(error):
        return (jsonify({"success": False, "error": 500, "message": "Internal server error"}), 500)


        
       

               

    return app
       

  
