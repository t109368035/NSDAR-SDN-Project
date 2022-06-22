import time
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog
from DBControll.ConnectDatabase import ConnectDatabase
from DBControll.RuleTable import RuleTable
from DBControll.UserTable import UserTable
from DBControll.NodeTable import NodeTable
from sdn_controller.SetRule import SetRule
from node_info.info_center import NodeINFO
from get_user.get_flow import Get_Live_Flow
from get_user.get_packet import Remote_capture
from ssh.power_controll import PowerControll

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        ##database
        ConnectDatabase()

        ##widget
        loadUi("workwidget\\tabletutorial.ui",self)
        self.tableWidget_userdata.setColumnWidth(0,350)
        self.tableWidget_userdata.setColumnWidth(1,350)
        self.tableWidget_nodeinfo.setColumnWidth(0,350)
        self.tableWidget_nodeinfo.setColumnWidth(1,350)
        self.ETT_Button.setEnabled(False)
        self.ETT_Button.clicked.connect(self.collect_ETT)
        self.loaddata_table_userdata()
        self.loaddata_table_nodeinfo()

        ##start node_info thread
        self.nodeinfo = NodeINFO()
        self.nodeinfo.start()
        self.nodeinfo.dpid_info.connect(self.loaddata_table_nodeinfo)
        self.nodeinfo.start_getpacket15.connect(self.start_getpacket15)
        self.nodeinfo.start_getpacket05.connect(self.start_getpacket05)
        self.nodeinfo.enable_ETT.connect(self.enable_ETT_button)

        ##start flag of get_user
        self.getpacket15_flag = False
        self.getpacket05_flag = False
        self.start_getflow15_flag = False
        self.start_getflow05_flag = False

#######
#collect ETT
#######
    def collect_ETT(self):
        print(self.nodeinfo.iperf_test_request())

    def enable_ETT_button(self, data):
        self.ETT_Button.setEnabled(True)

#######
#user info
#######
    def refresh_table_userdata(self, userdata):
        for user in userdata:
            SetRule().delete_rule(action='single user', ip=user)
        self.loaddata_table_userdata(condition=None)

    def check_start_getflow(self, condition):
        if condition == 'map15 start' and self.start_getflow15_flag is False:
            self.start_getflow15_flag = True
            #print('\n\n===========\nstart getflow15 : {}\n===========\n\n'.format(time.ctime()))
            self.get15flow = Get_Live_Flow('15')
            self.get15flow.start()
            self.get15flow.user_table_fresh.connect(self.refresh_table_userdata)
            self.get15flow.stop_getflow.connect(self.check_stop_getflow)
            self.get15flow.node_fail.connect(self.stop_getpacket)
        elif condition == 'map5 start' and self.start_getflow05_flag is False:
            self.start_getflow05_flag = True
            #print('\n\n===========\nstart getflow15 : {}\n===========\n\n'.format(time.ctime()))
            self.get05flow = Get_Live_Flow('5')
            self.get05flow.start()
            self.get05flow.user_table_fresh.connect(self.refresh_table_userdata)
            self.get05flow.stop_getflow.connect(self.check_stop_getflow)
            self.get05flow.node_fail.connect(self.stop_getpacket)

    def check_stop_getflow(self, condition):
        if condition == 'map15 stop' and self.start_getflow15_flag is True:
            print('\n\n===========\n{} getflow15\n===========\n\n'.format(condition))
            self.start_getflow15_flag = False
            self.get15flow.terminate()
        elif condition == 'map5 stop' and self.start_getflow05_flag is True:
            print('\n\n===========\n{} getflow05\n===========\n\n'.format(condition))
            self.start_getflow05_flag = False
            self.get05flow.terminate() 

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

#######
#node info
#######
    def stop_getpacket(self, node):
        PowerControll().node_reboot(node)
        NodeTable().delete_node(node)
        if node == 'map15' and self.getpacket15_flag is True: 
            self.getpacket15.terminate()    
            self.getpacket15_flag = False
            print('\n\n===========\nstop getpacket15 : {}\n===========\n\n'.format(time.ctime()))
        elif node == 'map5' and self.getpacket05_flag is True: 
            self.getpacket05.terminate()    
            self.getpacket05_flag = False
            print('\n\n===========\nstop getpacket05 : {}\n===========\n\n'.format(time.ctime()))

    def start_getpacket15(self, condition=None):
        dpid_rule = RuleTable().pop_dpid_rule(NodeTable().pop_node_info('map15')['node_dpid'])
        if dpid_rule and not self.start_getflow15_flag:
            SetRule().add_rule(rule_list=dpid_rule, re_add=True)
            self.check_start_getflow('map15 start')
        self.getpacket15_flag = True
        print('\n\n===========\nstart getpacket15 : {}\n===========\n\n'.format(time.ctime()))
        self.getpacket15 = Remote_capture('15')
        self.getpacket15.start()
        self.getpacket15.map_user.connect(self.loaddata_table_userdata)

    def start_getpacket05(self, condition=None):
        dpid_rule = RuleTable().pop_dpid_rule(NodeTable().pop_node_info('map5')['node_dpid'])
        if dpid_rule and not self.start_getflow05_flag:
            SetRule().add_rule(rule_list=dpid_rule, re_add=True)
            self.check_start_getflow('map5 start')
        self.getpacket05_flag = True
        print('\n\n===========\nstart getpacket05 : {}\n===========\n\n'.format(time.ctime()))
        self.getpacket05 = Remote_capture('5')
        self.getpacket05.start()
        self.getpacket05.map_user.connect(self.loaddata_table_userdata)

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
