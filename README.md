# Full Stack API Final Project
## Full Stack Trivia
[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

This project is the final project of my udacity session on API Development and Documentation. i've built an API  to finish the trivia app so it can hold :
1. Display questions - both all questions and by category. Questions show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

in this project, i hope i've sucessfully applied the skills learn in structuring and implementing well formatted API endpoints that leverage knowloedge of HTTP and API development best practices.
If not feel free to improve the code.

all backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).


## Getting Started
### Pre-requesites and Local Development
Developers trying to improve or using this project should already have python3, pip and node installed on ther local machines.

#### Backend
### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```
### Frontend
The directory contains a complete React frontend to consume the data from the Flask server.
From the frontend folder, run the following commands to start the client:
```bash
npm install // only once to install dependencies
npm start
```
By default, the frontend will run on localhost:3000.

## API Reference
### Getting Started
- Base URL: At present this app can only be run localy and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling
Errors are returned as JSON objects in the following format:
```bash
{
    "success": False,
    "error" : 400,
    "message": "bad request"
}
```
The API will three error types when requests fail, as:
- 400: Bad Request
- 404: Ressource Not Found
- 422: Not Processable

### Endpoints
### GET /categories
- General:
   - Returns a list of category objects and the success value
   - Result is formatted to be a set of key and value
- Sample : `curl http://127.0.0.1:5000/categories`

```
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
```
### GET /questions
- General:
   - Returns a list of question objects, the success value, a list of category objects, the current category and the total number of questions
   - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample : `curl http://127.0.0.1:5000/questions`
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "All",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": "5",
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": "5",
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": "4",
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": "5",
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": "4",
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": "6",
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": "6",
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "Lake Victoria",
      "category": "3",
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": "3",
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": "3",
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```
### DELETE /questions/{question_id}
- General:
   - Deletes the question of the given ID if it exists. Returns the id of the deleted question and the success value
- Sample : `curl -X DELETE http://127.0.0.1:5000/questions/10`
```
{
  "deleted": 15,
  "success": true
}
```
### POST /questions
- Genreral:
  - Creates a new question using the submitted question, answer, category, difficulty. Return the succes value.
- Sample : `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Who was the first president of Guinea", "answer":"Ahmed Sekou TOURE", "category":"4", "difficulty": 3}`
```
{
  "success": true
}
```

### GET /categories/{category_id}/questions
- General:
   - Returns a list of question objects by category of the given category ID, the success value, the current category and the total number of questions
   - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample : `curl http://127.0.0.1:5000/categories/2/questions`
```
{
  "current_category": "Art",
  "questions": [
    {
      "answer": "Escher",
      "category": "2",
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": "2",
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": "2",
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": "2",
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "success": true,
  "total_questions": 4
}
```
## Authors
Diawando DIAWARA

## Acknowledgements
the udacity slack's Full Stack community 


