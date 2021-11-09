'''
尚未完成:
在function:loaddata收到userdata之後，呼叫restful_api function讓使用者可以使用網路。

在function:loaddata裡，將userdata利用SLQ寫成database(db file)，
即可在snd_controller/open_all_channel_restful.py裡面加入讀取userdata的部分(記憶使用者)
'''
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("workwidget\\tabletutorial.ui",self)
        self.tableWidget.setColumnWidth(0,350)
        self.tableWidget.setColumnWidth(1,350)

    def loaddata(self, user_data):
        row=0
        self.tableWidget.setRowCount(len(user_data))

        sort_IP = sorted(user_data.keys())#按照順序排序
        for key in sort_IP:
            IP = QtWidgets.QTableWidgetItem(key)
            IP.setTextAlignment(QtCore.Qt.AlignCenter)
            
            MAC = QtWidgets.QTableWidgetItem(user_data[key])
            MAC.setTextAlignment(QtCore.Qt.AlignCenter)
            
            self.tableWidget.setItem(row, 0, IP)
            self.tableWidget.setItem(row, 1, MAC)
            
            row=row+1
