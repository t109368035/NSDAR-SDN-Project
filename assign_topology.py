from DBControll.ConnectDatabase import ConnectDatabase
from DBControll.LinkTable import LinkTable

ConnectDatabase()
#1
LinkTable().insert_link(start_node='mp11', end_node='mp13',bandwidth=60000000, ETX=1)
LinkTable().insert_link(start_node='mp13', end_node='mpp1',bandwidth=60000000, ETX=1)
#2
LinkTable().insert_link(start_node='map15', end_node='mp11',bandwidth=60000000, ETX=1)
LinkTable().insert_link(start_node='mp11', end_node='mp55',bandwidth=60000000, ETX=1)
LinkTable().insert_link(start_node='mp55', end_node='mp13',bandwidth=60000000, ETX=1)
LinkTable().insert_link(start_node='mp13', end_node='mpp98',bandwidth=60000000, ETX=1)
#3
LinkTable().insert_link(start_node='mpp98', end_node='mpp2',bandwidth=60000000, ETX=1)
#4
LinkTable().insert_link(start_node='mpp99', end_node='mpp3',bandwidth=60000000, ETX=1)
#5
LinkTable().insert_link(start_node='mpp99', end_node='mpp4',bandwidth=60000000, ETX=1)
LinkTable().insert_link(start_node='mpp89', end_node='mpp3',bandwidth=60000000, ETX=1)
#6
LinkTable().insert_link(start_node='mpp89', end_node='mpp4',bandwidth=60000000, ETX=1)
#7
LinkTable().insert_link(start_node='mpp88', end_node='mpp5',bandwidth=60000000, ETX=1)
#8
LinkTable().insert_link(start_node='map5', end_node='mp21',bandwidth=60000000, ETX=1)
LinkTable().insert_link(start_node='mp21', end_node='mp45',bandwidth=60000000, ETX=1)
LinkTable().insert_link(start_node='mp45', end_node='mp23',bandwidth=60000000, ETX=1)
LinkTable().insert_link(start_node='mp23', end_node='mpp88',bandwidth=60000000, ETX=1)
#9
LinkTable().insert_link(start_node='mp21', end_node='mp23',bandwidth=60000000, ETX=1)
LinkTable().insert_link(start_node='mp23', end_node='mpp6',bandwidth=60000000, ETX=1)