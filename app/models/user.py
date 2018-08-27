"""the User class reupresents a user of the system."""
from app.database import Database
import psycopg2
import json

class User(Database):

    def __init__(self, email, name, password):
        super().__init__()
        self.email = email
        self.name = name
        self.password = password

    """method inserts new user into db"""
    def insert_new_record(self):
        insert_command = "INSERT INTO users(email, name, password) VALUES('%s', '%s', '%s');" % (self.email, self.name, self.password,)
        try:
            self.cursor.execute(insert_command)
            self.cursor.execute("SELECT * FROM users WHERE email = '%s';" % (self.email,))
            item = self.cursor.fetchone()
            return item
        except psycopg2.IntegrityError:
            output = {
                'message': 'Email address already exists: ',
            }
            return output

    """deletes users from db"""
    def delete_user_from_db(self):
        delete_command = "DELETE FROM users WHERE email = %s;", (self.email,)
        self.cursor.execute(delete_command)

    def query_single(self):
        self.cursor.execute("SELECT * FROM users WHERE email = '%s'" % (self.email))
        items = self.cursor.fetchone()
        return items
        