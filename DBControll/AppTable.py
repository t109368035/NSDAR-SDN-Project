from DBControll.DBConnection import DBConnection


class AppTable:
    def insert_a_app(self, user_ip, app_name, app_ip):
        command = "INSERT INTO app_table (user_ip, app_name, app_ip) VALUES  ('{}', '{}', '{}');".format(user_ip, app_name, app_ip)
            
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def delete_user_app(self, user_ip):
        command = "DELETE FROM app_table WHERE user_ip='{}';".format(user_ip)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def delete_all(self):
        command = "DELETE FROM app_table;"

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

"""
    def pop_user_rule(self, user_ip):
        command = "SELECT * FROM rule_table WHERE user_ip='{}';".format(user_ip)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()

        return [row['user_rule'] for row in record_from_db]

"""