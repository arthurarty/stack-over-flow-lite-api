from datetime import datetime
from flask import jsonify
from app.database import Database
import psycopg2
"""Class Answer represents an answer to a question
"""
class Answer(Database): 

    def __init__(self, question_id, title, user_id):
        super().__init__()
        self.question_id = question_id
        self.title = title
        self.user_id = user_id
        self.preferred = 'false'
        self.date = str(datetime.now())

    def return_question_id(self):
        return self.question_id

    def return_answer_author(self):
        return self.user_id

    def return_answer_date(self):
        return self.date

    def return_answer_title(self):
        return self.title
    
    """method inserts new question into db"""
    def insert_new_record(self):
        insert_command = "INSERT INTO answers(question_id, user_id, title, preferred, created_at) VALUES('%s', '%s', '%s', '%s','%s');" % (self.question_id, self.user_id, self.title, self.preferred, self.date,)
        try:
            self.cursor.execute(insert_command)
            self.cursor.execute("SELECT row_to_json(row) FROM (SELECT * FROM answers WHERE question_id = '%s') row;" % (self.question_id,))
            items = self.cursor.fetchall()
            return jsonify(items), 201
        except psycopg2.IntegrityError as e:
            output = { 
                'message': '%s' % e,
            }
            return jsonify(output), 404

        