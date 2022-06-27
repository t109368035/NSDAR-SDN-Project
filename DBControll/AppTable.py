from DBControll.DBConnection import DBConnection


class AppTable:
    def insert_a_app(self, AP, stime, user_ip, user_port, server_name, 
                    server_ip, server_port, protocol_L4, 
                    protocol_L7, first_seen, last_seen, duration, bytes):
        command = "INSERT INTO app_table (AP, stime, user_ip, user_port, server_name, server_ip, server_port, protocol_L4, protocol_L7, first_seen, last_seen, duration, bytes) VALUES  ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(AP, stime, user_ip, user_port, server_name, server_ip, server_port, protocol_L4, protocol_L7, first_seen, last_seen, duration, bytes)
            
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def delete_AP_app(self, AP):
        command = "DELETE FROM app_table WHERE AP='{}';".format(AP)

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
