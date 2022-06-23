from DBControll.DBConnection import DBConnection

class PathTable:
    def insert_path(self, AP, app_type, path):
        command = "INSERT INTO path_table (AP, app_type, path) VALUES  ('{}', '{}', '{}');".format(AP, app_type, path)
            
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def pop_AP_type_path(self, AP, app_type):
        command = "SELECT * FROM path_table WHERE AP='{}' AND app_type='{}';".format(AP, app_type)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchone()
        return record_from_db['path ']
    
    def pop_AP_path(self, AP):
        command = "SELECT * FROM path_table WHERE AP='{}';".format(AP)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchone()

        return [row['path'] for row in record_from_db]
        
    def pop_all_path(self):
        command = "SELECT * FROM path_table;"

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()

        return [row['path'] for row in record_from_db]
    
    def delete_type_path(self, app_type):
        command = "DELETE FROM path_table WHERE app_type='{}';".format(app_type)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def delete_all(self):
        command = "DELETE FROM path_table;"

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()
