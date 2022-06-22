from DBControll.DBConnection import DBConnection

class NodeTable:
    def insert_node(self, node_name, node_dpid, node_mac):
        command = "INSERT INTO node_table (node_name, node_dpid, node_mac) VALUES  ('{}', '{}', '{}');".format(node_name, node_dpid, node_mac)
            
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()
    
    def pop_node_info(self, node_name):
        command = "SELECT * FROM node_table WHERE node_name='{}';".format(node_name)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchone()

        if not record_from_db:
            return None
        else:
            return {'node_name': record_from_db['node_name'], 'node_mac': record_from_db['node_mac'], 'node_dpid': record_from_db['node_dpid']}
        
    def pop_all_node(self):
        command = "SELECT * FROM node_table;"

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()

        return [row['node_name'] for row in record_from_db]
    
    def delete_node(self, node_name):
        command = "DELETE FROM node_table WHERE node_name='{}';".format(node_name)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def delete_all(self):
        command = "DELETE FROM node_table;"

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()
    '''
    def select_a_patient(self, bed_id):
            command = "SELECT * FROM patient_list WHERE bed_id='{}'".format(bed_id)

            with DBConnection() as connection:
                cursor = connection.cursor()
                cursor.execute(command)
                record_from_db = cursor.fetchall()

            return [row['bed_id'] for row in record_from_db]

    def select_all_patient(self):
            command = "SELECT * FROM patient_list"

            with DBConnection() as connection:
                cursor = connection.cursor()
                cursor.execute(command)
                record_from_db = cursor.fetchall()

            return [row['bed_id'] for row in record_from_db]
    '''