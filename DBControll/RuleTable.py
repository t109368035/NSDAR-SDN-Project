from DBControll.DBConnection import DBConnection


class RuleTable:
    def insert_a_rule(self, user_ip, user_rule, status):
        command = "INSERT INTO rule_table (user_ip, user_rule, status) VALUES  ('{}', '{}', '{}');".format(user_ip, user_rule, status)
            
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