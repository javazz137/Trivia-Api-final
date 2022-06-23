# Trivia App

The application:

1. Display questions - both all questions and by category.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.


## Getting started

We started the full stack application for you. It is designed with some key functional areas:

### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file.

1. `export FLASK_APP=flaskr`
2. `export FLASK_ENV=development`
3. `flask run`

These commands put the application in development and directs our application to use the __init__.py file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the Flask documentation.

The application is run on http://127.0.0.1:5000/ by default and is a proxy in the frontend configuration.

### Frontend

From the frontend folder, run the following commands to start the client:
`npm install` // only once to install dependencies
`npm start`

## API reference

### Getting started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling
Errors are returned as JSON objects in the following format:
```json
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

The API will return three error types when requests fail:

400: Bad Request
404: Resource Not Found
422: Not Processable


### Endpoints
`GET /categories`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.
Sample: `curl http://127.0.0.1:5000/categories`

```json
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

`GET /questions`

- Returns a list of question objects, success value, and total number of questions
- Include an optional request argument to choose a desired page number, starting from 1.
- Results are paginated in groups of 10.

Sample: `curl http://127.0.0.1:5000/questions`

```json
 { "questions": [
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
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    ], 
  "success": true, 
  "total_questions": 3
}
```

`DELETE /questions/{question_id}`

- Deletes a question if it exists.
- Request Argument: question_id
- Returns the id of the deleted question, success value, total questions now available.

Sample: `curl -X DELETE http://127.0.0.1:5000/question/5`

```json
{
  "deleted": 5, 
  "success": true, 
  "total_questions": 2
}
```

`POST /questions`

- Creates a new question using the submitted question, answer, category and difficulty.
- Request Arguments: question, answer, category and difficulty.
- Returns the id of the created question, questions list based on current page number to update the frontend, success value, and the total questions now available.

Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Which Dutch graphic artist was a creator of optical illusions?", "answer":"Jesus", "category":"2", "difficulty":"1"}'`

```json
{
  "created": 42, 
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
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ], 
  "success": true, 
  "total_questions": 3
}
```

`POST /questions/search`

- Searches for questions using the searchTerm. The search term must be a substring of the question.
- Request parameter: searchTerm.
- This endpoint returns a list of questions object to update the frontend, success value, and the total number of questions gotten from the search. 
- Each question object include, the id of the question returned, question, answer, category and difficulty,  

Sample: `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"actor"}'`

```json
{
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```

`GET /categories/{categories_id}/questions`

- Returns, the category requested, a list of questions object in that category, a success value and the number of questions in that category.

Sample: `curl http://127.0.0.1:5000/categories/1/questions`

```json
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
    },
    ], 
  "success": true, 
  "total_questions": 3
}
```

`POST /quizzes`

- Returns a random question object within the given category that is not one of the previous questions and a success value.
- Request parameters:  category, previous question parameters
- The random question object includes, the question, id, difficulty, answer and category. The request parameters are optional.

Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_question" :[1], "quiz_category" : {"id": 1}}'`
```json
{
  "question": {
    "answer": "Blood", 
    "category": 1, 
    "difficulty": 4, 
    "id": 22, 
    "question": "Hematology is a branch of medicine involving the study of what?"
  }, 
  "success": true
}
```


## Deployment N/A

## Authours
Jabulani Ngwenyama

## Acknowledgements
Udacity Team and My session lead Faithful Ojebiyi.
