"""This file contains the database class that contains all database related methods"""
import psycopg2
from pprint import pprint
from urllib.parse import urlparse
class Database:
    def __init__(self):
        try:
            result = urlparse("postgresql://localhost/stack")
            username = 'postgres'
            password = 'asP2#fMe'
            database = result.path[1:]
            hostname = result.hostname
            portno = 5432
            self.connection = psycopg2.connect(
            database = database,
            user = username,
            password = password,
            host = hostname,
            port = portno
            )
            #self.connection = psycopg2.connect("dbname=stack user=postgres password=asP2#fMe")
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except:
            pprint("Cannot connect to database")

    def create_table(self, table_name, table_columns):
        """method creates a single table"""
        create_table_command = "CREATE TABLE %s(%s);" % (table_name, table_columns)
        self.cursor.execute(create_table_command)
    
    def drop_table(self, table_name):
        """method drops a single table from the database"""
        drop_table_command = "DROP TABLE %s" % (table_name)
        self.cursor.execute(drop_table_command)

    def insert_new_record(self):
        """method to be overriden by classes inheriting"""
        pass

    def query_single(self, email):
        """returns a user given the user's email"""
        self.cursor.execute("SELECT * FROM users WHERE email = '%s'" % (email))
        item = self.cursor.fetchone()
        return item

    def query_single_row(self, table_name, table_column, row_id):
        """returns a single row from table_name where table_column = row_id"""
        self.cursor.execute("SELECT row_to_json(row) FROM (SELECT * FROM %s WHERE %s = '%s') row" % (table_name, table_column, row_id))
        item = self.cursor.fetchone()
        return item

    def query_all(self, table_name):
        """queries a table for all its records"""
        self.cursor.execute("SELECT row_to_json(row) FROM (SELECT * FROM %s) row;" % (table_name))
        items = self.cursor.fetchall()
        return items
    
    def query_all_where_id(self, table_name, table_column, item_id):
        """method selects all records from a database mathching a value
        select * from table_name where table_column = item_id"""
        self.cursor.execute("SELECT row_to_json(row) FROM (SELECT * FROM %s WHERE %s = '%s')row;" % (
            table_name, table_column, item_id))
        items = self.cursor.fetchall()
        return items

    def update_record(self, table_name, set_column, new_value, where_column, item_id):
        """method updates record. i.e UPDATE table_name SET set_column = new_value, where
        where_colum = item_id"""
        update_command = "Update %s SET %s = '%s' WHERE %s = '%s'" % (table_name, 
        set_column, new_value, where_column, item_id)
        self.cursor.execute(update_command)


    def return_id(self, email):
        """method returns users's id from databse"""
        self.cursor.execute("SELECT user_id FROM users WHERE email = '%s'" % (email))
        item = self.cursor.fetchone()
        return item
    
    def return_password(self, email):
        """method returns uers's hashed password from database"""
        self.cursor.execute("SELECT password FROM users WHERE email = '%s'" % (email))
        item = self.cursor.fetchone()
        return item

    def create_all_tables(self):
        """method creates the tables needed for the application"""
        self.create_table('users', "user_id SERIAL PRIMARY KEY, email text " + 
        " NOT NULL UNIQUE, name text NOT NULL, password text NOT NULL")

        self.create_table('questions', "question_id SERIAL PRIMARY KEY," + 
        "user_id int NOT NULL REFERENCES users(user_id),title text NOT NULL UNIQUE," + 
        "created_at date NOT NULL")

        self.create_table('answers', "answer_id SERIAL PRIMARY KEY," + 
        "question_id int NOT NULL REFERENCES questions(question_id)," + 
        "user_id int NOT NULL REFERENCES users(user_id), title text " + 
        "NOT NULL, preferred boolean, created_at date NOT NULL")

    def drop_all_tables(self):
        """method drops all tables from database"""
        self.drop_table("answers")
        self.drop_table("questions")
        self.drop_table("users")

    def delete_question(self, question_id):
        """method deletes question from database"""
        delete_answers = "DELETE FROM answers WHERE question_id = %s" % (question_id)
        self.cursor.execute(delete_answers)
        delete_command = "DELETE FROM questions WHERE question_id = %s" % (question_id)
        self.cursor.execute(delete_command)

    def return_user_id(self, table_name, where_column, row_id):
        user_id_command = "SELECT user_id FROM %s WHERE %s = %s" % (table_name, where_column, row_id)
        self.cursor.execute(user_id_command)
        user_id = self.cursor.fetchone()
        return user_id

#db = Database()
#item = db.return_password("arthur@truit.com")
#print(item[0])
# print(db.return_user_id_question(2))
