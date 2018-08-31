"""The module contains the Question class"""
from datetime import datetime
from app.database import Database
from flask import jsonify
import psycopg2


class Question(Database):

    def __init__(self, user_id, title):
        """initializes an instance of class question"""
        super().__init__()
        self.user_id = user_id
        self.title = title
        self.date = datetime.now()

    def insert_new_record(self):
        """method inserts new question into db"""
        insert_command = "INSERT INTO questions(user_id, title, created_at) VALUES('%s', '%s', '%s');" % (
            self.user_id, self.title, self.date,)
        try:
            self.cursor.execute(insert_command)
            self.cursor.execute(
                " SELECT row_to_json(row) FROM (SELECT * FROM questions WHERE title = '%s') row;" % (self.title,))
            items = self.cursor.fetchone()
            if items:
                return jsonify({"msg": "Question Successfully added"}), 201
            return jsonify({"msg": "Question not added"}), 400
        except psycopg2.IntegrityError:
            return jsonify({"msg": "Question already exists in the database"}), 404
