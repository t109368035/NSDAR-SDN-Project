from DBControll.DBConnection import DBConnection


class RuleTable:
    def insert_a_rule(self, AP, app_type, user_ip, user_rule, node_name):
        command = "INSERT INTO rule_table (AP, app_type, user_ip, user_rule, node_name) VALUES  ('{}', '{}', '{}', '{}', '{}');".format(AP, app_type, user_ip, user_rule, node_name)
            
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def pop_user_rule(self, user_ip):
        command = "SELECT * FROM rule_table WHERE user_ip='{}';".format(user_ip)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()

        return [row['user_rule'] for row in record_from_db]

    def delete_user_rule(self, user_ip):
        command = "DELETE FROM rule_table WHERE user_ip='{}';".format(user_ip)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def pop_node_rule(self, node_name):
        command = "SELECT * FROM rule_table WHERE node_name='{}';".format(node_name)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()

        return [row['user_rule'] for row in record_from_db]

    def delete_all(self):
        command = "DELETE FROM rule_table;"

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()
    
    def pop_all_rule(self):
        command = "SELECT * FROM rule_table"

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()

        return [row['user_rule'] for row in record_from_db]