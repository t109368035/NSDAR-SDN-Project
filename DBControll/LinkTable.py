from DBControll.DBConnection import DBConnection

class LinkTable:
    def insert_link(self, start_node, end_node, bandwidth, ETX):
        command = "INSERT INTO link_table (start_node, end_node, bandwidth, ETX) VALUES  ('{}', '{}', '{}', '{}');".format(start_node, end_node, bandwidth, ETX)
            
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def pop_ETT(self):
        command = "SELECT * FROM link_table;"

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()
        
        packetsize = 12112
        return [(row['start_node'], row['end_node'], row['ETX']*(packetsize/row['bandwidth'])) for row in record_from_db]
    
    def pop_ETX(self):
        command = "SELECT * FROM link_table;"

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()

        return [(row['start_node'], row['end_node'], row['ETX']) for row in record_from_db]

    def pop_all_link(self):
        command = "SELECT * FROM link_table;"

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()
        
        return [[row['start_node'], row['end_node'], row['bandwidth'], row['ETX']] for row in record_from_db]

    def delete_link(self, start_node, end_node):
        command = "DELETE FROM link_table WHERE start_node='{}' AND end_node='{}';".format(start_node, end_node)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def modify_bandwidth(self, start_node, end_node, bandwidth):
        command = "UPDATE link_table SET bandwidth='{}' WHERE start_node='{}' AND end_node='{}';".format(bandwidth, start_node, end_node)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def modify_ETX(self, start_node, end_node, ETX):
        command = "UPDATE link_table SET ETX='{}' WHERE start_node='{}' AND end_node='{}';".format(ETX, start_node, end_node)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def pop_link_start_with(self, start_node):
        command = "SELECT * FROM link_table WHERE start_node='{}';".format(start_node)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()
        try:
            return [[row['start_node'], row['end_node']] for row in record_from_db]
        except:
            return None

    def pop_link_end_with(self, end_node):
        command = "SELECT * FROM link_table WHERE end_node='{}';".format(end_node)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()
        try:
            return [[row['start_node'], row['end_node']] for row in record_from_db]
        except:
            return None
            
    def pop_bandwidth(self, start_node, end_node):
        command = "SELECT * FROM link_table WHERE start_node='{}' AND end_node='{}';".format(start_node, end_node)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchone()
        return record_from_db['bandwidth']
    
    def pop_uETX(self, start_node, end_node):
        command = "SELECT * FROM link_table WHERE start_node='{}' AND end_node='{}';".format(start_node, end_node)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchone()
        return record_from_db['ETX']
    
    def pop_ETT_single(self, start_node, end_node):
        command = "SELECT * FROM link_table WHERE start_node='{}' AND end_node='{}';".format(start_node, end_node)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchone()
        packetsize = 12112
        return record_from_db['ETX']*(packetsize/record_from_db['bandwidth'])

    def delete_all(self):
        command = "DELETE FROM link_table;"

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()