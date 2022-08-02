from DBControll.ConnectDatabase import ConnectDatabase
from DBControll.LinkTable import LinkTable

ConnectDatabase()
original_link = LinkTable().pop_all_link()
LinkTable().delete_all()
for link in original_link:
    LinkTable().insert_link(start_node=link[0], end_node=link[1],
                            bandwidth=60000000, ETX=link[3])