"""The module contains the Question class"""
from datetime import datetime
from app.database import Database
from flask import jsonify
import psycopg2

class Question(Database):

    def __init__(self, user_id, title):
        super().__init__()
        self.user_id = user_id
        self.title = title
        self.date = datetime.now()

    """returns user id"""
    def return_user_id(self):
        return self.user_id

    """method inserts new question into db"""
    def insert_new_record(self):
        insert_command = "INSERT INTO questions(user_id, title, created_at) VALUES('%s', '%s', '%s');" % (self.user_id, self.title, self.date,)
        try:
            self.cursor.execute(insert_command)
            self.cursor.execute(" SELECT row_to_json(row) FROM (SELECT * FROM questions WHERE title = '%s') row;" % (self.title,))
            items = self.cursor.fetchone()
            return jsonify(items), 201
        except psycopg2.IntegrityError as e:
            output = { 
                'message': '%s' % e,
            }
            return jsonify(output), 404