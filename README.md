[![Build Status](https://travis-ci.com/arthurarty/stack-over-flow-lite-api.svg?branch=develop)](https://travis-ci.com/arthurarty/stack-over-flow-lite-api)
[![Coverage Status](https://coveralls.io/repos/github/arthurarty/stack-over-flow-lite-api/badge.svg?branch=develop)](https://coveralls.io/github/arthurarty/stack-over-flow-lite-api?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/841bea4173538cb7329b/maintainability)](https://codeclimate.com/github/arthurarty/stack-over-flow-lite-api/maintainability)

## stack-over-flow-lite-api 
# Description

StackOverFLow-lite is an api through which users can login, view all questions with their respective answers, post questions and get answers from other users.  
# Link to application to api documentation: 
https://stackarty.herokuapp.com/
# Link to demo on heroku application
https://stackarty.herokuapp.com

# Requirements
* `Python 3.5` or greater : Python is interpreted high-level programming language for general-purpose programming. 
* `FLask` : Flask is a micro web framework written in Python.
* `Flask-JWT-Extended` : A flask extension that makes it easy to protect endpoints using jwt tokens. 
* `Postgres Sql` : An open source relational database management system ( DBMS )
* `psycopg2` : PostgreSQL adapter for the Python programming language. 

# Installation
```
$git clone https://github.com/arthurarty/stack-over-flow-lite-api
$cd stack-over-flow-lite-api
$python database_setup.py
$python run.py
```

Project Overview
--------------------------------
|Endpoint |Functionality |Note |
|---------|:------------:|:---:|
|POST /auth/signup|Register a user| |
|POST /auth/login |Login a user | |
|GET /questions |Fetch all questions | |
|GET /questions/<questionId>|Fetch a specific question|This should come with the all  answers provided so far for the question.
|GET /questions/user | Fetch all questions for a specific user. | User can only get his questions. 
|POST /questions|Post a question| |
|Delete /questions/<questionId>|Delete a question| This endpoint should be available to the author’s author.
|POST /questions/<questionId>/answers|Post an answer to a question| |
|PUT /questions/<questionId>/answers/<answerId> | Mark an answer as accepted or update an answer. |This endpoint should be available to only the answer author and question author. The answer author calls the route to update answer while the question author calls the route to accept answer.
 
