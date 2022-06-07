from tabnanny import check
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog
from DBControll.ConnectDatabase import ConnectDatabase
from DBControll.UserTable import UserTable
from DBControll.NodeTable import NodeTable
from sdn_controller.SetRule import SetRule
from get_user.get_flow import Get_Live_Flow

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("workwidget\\tabletutorial.ui",self)
        self.tableWidget_userdata.setColumnWidth(0,350)
        self.tableWidget_userdata.setColumnWidth(1,350)
        self.tableWidget_nodeinfo.setColumnWidth(0,350)
        self.tableWidget_nodeinfo.setColumnWidth(1,350)
        ConnectDatabase()
        self.loaddata_table_userdata()
        self.loaddata_table_nodeinfo()
        self.start_getflow15_flag = False

    def refresh_table_userdata(self, userdata):
        for user in userdata:
            SetRule().delete_rule(action='single user', ip=user)
        self.loaddata_table_userdata(condition=None)

    def check_start_getflow(self, condition):
        if condition == 'add15' and self.start_getflow15_flag is False:
            self.start_getflow15_flag = True
            print('\n\n===========\nstart getflow15\n===========\n\n')
            self.get15flow = Get_Live_Flow('15')
            self.get15flow.start()
            self.get15flow.user_table_fresh.connect(self.refresh_table_userdata)
            self.get15flow.stop_getflow.connect(self.check_stop_getflow)
    
    def check_stop_getflow(self, condition):
        if condition == 'map15 stop' and self.start_getflow15_flag is True:
            self.start_getflow15_flag = False
            self.get15flow.terminate() 

    def loaddata_table_userdata(self, condition=None):
        self.check_start_getflow(condition)
        user_list = UserTable().pop_all_user()
        if user_list:
            row=0
            self.tableWidget_userdata.setRowCount(len(user_list))
            sort_IP = sorted(user_list)#按照順序排序
            for IP in sort_IP:
                user_info = UserTable().pop_user_info(IP)
                IP = QtWidgets.QTableWidgetItem(user_info['user_ip'])
                IP.setTextAlignment(QtCore.Qt.AlignCenter)
                MAC = QtWidgets.QTableWidgetItem(user_info['user_mac'])
                MAC.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget_userdata.setItem(row, 0, IP)
                self.tableWidget_userdata.setItem(row, 1, MAC)
                row=row+1
        else:
            self.tableWidget_userdata.setItem(0, 0, None)
            self.tableWidget_userdata.setItem(0, 1, None)

    def loaddata_table_nodeinfo(self, dpid_data=None):
        node_list = NodeTable().pop_all_node()
        if node_list:
            self.tableWidget_nodeinfo.setRowCount(len(node_list))
            row=0
            sort_dpid = sorted(node_list)#按照順序排序
            for node_ID in sort_dpid:
                node_info = NodeTable().pop_node_info(node_ID)
                node_name = QtWidgets.QTableWidgetItem(node_info['node_name'])
                node_name.setTextAlignment(QtCore.Qt.AlignCenter)
                node_dpid = QtWidgets.QTableWidgetItem(node_info['node_dpid'])
                node_dpid.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget_nodeinfo.setItem(row, 0, node_name)
                self.tableWidget_nodeinfo.setItem(row, 1, node_dpid)
                row=row+1
