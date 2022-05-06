'''
尚未完成:
在function:loaddata收到userdata之後，呼叫restful_api function讓使用者可以使用網路。
'''
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog
from DBControll.ConnectDatabase import ConnectDatabase
from DBControll.UserTable import UserTable
from DBControll.NodeTable import NodeTable

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("workwidget\\tabletutorial.ui",self)
        self.tableWidget_userdata.setColumnWidth(0,350)
        self.tableWidget_userdata.setColumnWidth(1,350)
        
        self.tableWidget_nodeinfo.setColumnWidth(0,350)
        self.tableWidget_nodeinfo.setColumnWidth(1,350)
        
        self.tableWidget_iwinfo.setColumnWidth(0,300)
        self.tableWidget_iwinfo.setColumnWidth(1,200)
        self.tableWidget_iwinfo.setColumnWidth(2,200)
        
        ConnectDatabase()
        self.loaddata_table_userdata()
        self.loaddata_table_nodeinfo()

    def loaddata_table_userdata(self, user_data=None):
        user_list = UserTable().pop_all_user()
        if user_list:
            self.tableWidget_userdata.setRowCount(len(user_list))
            row=0
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

    def loaddata_table_iwinfo(self, iw_data):
        row = 0
        self.tableWidget_iwinfo.setRowCount(len(iw_data))
        #print(iw_data)
        sort_pathid = sorted(iw_data.keys())#按照順序排序
        for key in sort_pathid:
            #print(iw_data[key]['tx_bitrate'])
            #print(iw_data[key]['signal'])
            path_ID = QtWidgets.QTableWidgetItem(key)
            path_ID.setTextAlignment(QtCore.Qt.AlignCenter)

            tx_rate = QtWidgets.QTableWidgetItem(str(iw_data[key]['tx_bitrate']))
            tx_rate.setTextAlignment(QtCore.Qt.AlignCenter)

            rssi = QtWidgets.QTableWidgetItem(str(iw_data[key]['signal']))
            rssi.setTextAlignment(QtCore.Qt.AlignCenter)

            self.tableWidget_iwinfo.setItem(row, 0, path_ID)
            self.tableWidget_iwinfo.setItem(row, 1, tx_rate)
            self.tableWidget_iwinfo.setItem(row, 2, rssi)

            row=row+1