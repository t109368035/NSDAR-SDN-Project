import os, sys
sub_path = os.path.abspath(os.getcwd())
path = sub_path.replace('NSDAR_optimize_simulation', '')
sys.path.insert(0, path)
from DBControll.ConnectDatabase import ConnectDatabase
from DBControll.LinkTable import LinkTable
os.chdir(path)

ConnectDatabase()
original_link = LinkTable().pop_all_link()
LinkTable().delete_all()
for link in original_link:
    LinkTable().insert_link(start_node=link[0], end_node=link[1],
                            bandwidth=70000000, ETX=1)