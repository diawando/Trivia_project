import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
# function to paginate questions
def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    
    return current_questions

# function to render categories as a dict 
def categories_conveter(ElementToConvert):
    categories_formated = [category.format() for category in ElementToConvert]
    categories = {}
    for category in categories_formated:
        categories[category['id']] = category['type']
    return categories
  
  
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  CORS(app)
  # after_request decorator to set Access-Control-Allow
  @app.after_request
  def after_request(response):
     response.headers.add(
       "Access-Control-Allow-Headers", "Content-Type, Authorization,true"
     )
     response.headers.add(
       "Access-Control-Allow-Methods", "GET, PUT, POST, DELETE, OPTIONS"
     )
     return response
  
  
  #Endpoint to retrieve categories
  @app.route('/categories')
  def retrieve_categories():
      selection = Category.query.order_by(Category.id).all()
      if len(selection)== 0:
          abort(404)
          
      categories = categories_conveter(selection)
      
      return jsonify({
          "success" : True,
          "categories": categories
      })
 
 #Endpoint to retrieve question
  @app.route('/questions')
  def retrieve_questions():
      selection = Question.query.order_by(Question.id).all()
      categories = Category.query.order_by(Category.id).all()
      questions = paginate_questions(request, selection)
      
      if len(questions) == 0:
          abort(404)
     
      return jsonify({
           "success" : True,
           "questions" : questions,
           "categories": categories_conveter(categories),
           "current_category" : 'All',
           "total_questions": len(selection)
      })
   
   
  #Endpoint to Delete question   
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
      question = Question.query.get(question_id)
      try:
        
         question.delete()
        
         return jsonify(
          {
            "success": True,
            "deleted": question_id
          }
          )
      
      except:
          abort(422)
          
  #Endpoint to create question
  @app.route('/questions', methods=['POST'])
  def create_question():
      body = request.get_json()
      
      try:
        
          new_question = body.get("question", None)
          new_answer = body.get("answer", None)
          new_category = body.get("category", None)
          new_difficulty = body.get("difficulty", None)
          
          if new_question == "" or new_answer == "":
              abort(422)
          
          question = Question(
              question = new_question,
              answer = new_answer,
              category = new_category,
              difficulty = new_difficulty 
          )

          question.insert()
          
          return jsonify({
              "success" : True,
          })
      except:
         abort(422)
         
         
  #Endpoint search for a question
  @app.route('/questions', methods=['POST'])
  def search_questions():
      body = request.get_json()
      
      search_term = body.get("searchTerm", None)
      
      if search_term :
          selection = Question.query.order_by(Question.id).filter(
                        Question.question.ilike("%{}%").format(search_term)
                      ).all()
          questions = paginate_questions(request, selection)
          
          return jsonify(
            {
              "success": True,
              "questions": questions,
              "current_category":"all",
              "total_questions": len(selection)
            }
          )
      else:
          abort(404)
       
  #Endpoin to show questions based on category
  @app.route('/categories/<int:category_id>/questions')
  def questions_by_category(category_id):
    
      selection = Question.query.order_by(Question.id).filter(Question.category == str(category_id)).all()
      category = Category.query.get(category_id)
      
      current_questions = paginate_questions(request, selection)
      
      if len(selection) == 0:
         abort(404)
      
      return jsonify({
          "success" : True,
          "questions": current_questions,
          "current_category": category.type,
          "total_questions": len(selection)
      })

  @app.route('/quizzes', methods=['POST'])
  def launc_quiz():
      body = request.get_json()

      previous_questions = body.get("previous_questions", None)
      quiz_category = body.get("quiz_category", None)
      if quiz_category is None:
          abort(422)
      if quiz_category['id'] != 0 :   
          selection = Question.query.order_by(Question.id).filter(
                     Question.category == quiz_category['id']).filter(
                        Question.id not in previous_questions
                      ).all()
          questions = [question.format() for question in selection]
      
          question = random.choice(questions)
      
          return jsonify(
            {
                "success": True,
                "question": question
          }
            )
      else :
            selection = Question.query.order_by(Question.id).filter(Question.id not in previous_questions).all()
            
            questions = [question.format() for question in selection]
            
            question = random.choice(questions)
            
            return jsonify(
              {
                  "success": True,
                  "question": question
              }
              ) 
        
 # Error Handler
  @app.errorhandler(404)
  def resource_not_found(error):
     return jsonify(
       {
         "success": False,
         "error" : 404,
         "message": "resource not found"
       }
     ), 404
     
  @app.errorhandler(400)
  def bad_request(error):
      return jsonify(
        {
          "success": False,
          "error": 400,
          "message": "bad request"
        }
      ), 400
  
  @app.errorhandler(405)
  def method_not_allowed(error):
      return jsonify(
        {
          "success": False,
          "error" : 405,
          "message": "method not allowed"
        }
      ), 405

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify(
        {
          "success" : False,
          "error" : 422,
          "message" : "unprocessable",
        }
      ), 422
      
  @app.errorhandler(500)
  def server_error(error):
      return jsonify(
        {
          "success": False,
          "error" : 500,
          "message" : "internal server error"
      }
        ), 500
  return app

    