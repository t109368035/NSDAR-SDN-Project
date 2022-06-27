from DBControll.DBConnection import DBConnection


necessary_table_to_create = {
    "path_table":
        """
            CREATE TABLE path_table
            (
                AP VARCHAR(255),
                app_type VARCHAR(255),
                path VARCHAR(255),
                vlan VARCHAR(255)
            );
        """,

    "link_table":
        """
            CREATE TABLE link_table
            (
                start_node VARCHAR(255),
                end_node VARCHAR(255),
                bandwidth FLOAT,
                ETX FLOAT
            );
        """,

    "node_table":
        """
            CREATE TABLE node_table
            (
                node_name VARCHAR(255) PRIMARY KEY,
                node_dpid VARCHAR(255),
                node_mac VARCHAR(255)
            );
        """,

    "user_table":
        """
            CREATE TABLE user_table
            (
                user_ip VARCHAR(255) PRIMARY KEY,
                user_mac VARCHAR(255),
                user_vlan VARCHAR(255),
                user_path VARCHAR(255),
                user_type VARCHAR(255),
                user_ap VARCHAR(255)
            );
        """,

    "rule_table":
        """
            CREATE TABLE rule_table
            (
                AP VARCHAR(255), 
                app_type VARCHAR(255),
                user_ip VARCHAR(255),
                user_rule VARCHAR(255),
                node_name VARCHAR(255)
            );
        """,
    
    "app_table":
        """
            CREATE TABLE app_table
            (
                AP VARCHAR(255),
                stime VARCHAR(255),
                user_ip VARCHAR(255),
                user_port VARCHAR(255),
                server_name VARCHAR(255),
                server_ip VARCHAR(255),
                server_port VARCHAR(255),
                protocol_L4 VARCHAR(255),
                protocol_L7 VARCHAR(255),
                first_seen VARCHAR(255),
                last_seen VARCHAR(255),
                duration VARCHAR(255),
                bytes VARCHAR(255)
            );
        """
}


class DBInitializer:
    def execute(self):
        existing_tables = self.get_existing_tables()
        self.__create_inexist_table(existing_tables)

    def get_existing_tables(self):
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM sqlite_master WHERE type='table'")
            records = cursor.fetchall()

        return [single_row["tbl_name"] for single_row in records]

    def __create_inexist_table(self, existing_tables):
        for necessary_table, table_creating_command in necessary_table_to_create.items():
            if necessary_table not in existing_tables:
                self.create_table_with_specefied_command(table_creating_command)

    def create_table_with_specefied_command(self, command):
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()