from app.database import Database


def set_up():
    db = Database()
    db.create_all_tables()


def tear_down():
    db = Database()
    db.drop_all_tables()


set_up()
