from DBControll.DBConnection import DBConnection
from DBControll.DBInitializer import DBInitializer

class ConnectDatabase():
    def __init__(self):
        DBConnection.db_file_path = "DBControll\\database.db"
        DBInitializer().execute()
