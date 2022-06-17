import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from workwidget.main_widget import MainWindow
from sdn_controller.excute_ryu import Excute_ryu
from node_info.info_center import MQTT
from sdn_controller.SetRule import SetRule
from DBControll.AppTable import AppTable


class Mainapp:
    def __init__(self):
        app = QApplication(sys.argv)
        mainwindow = MainWindow()
        widget = QtWidgets.QStackedWidget()
        widget.addWidget(mainwindow)
        widget.setFixedHeight(850)
        widget.setFixedWidth(1120)
        widget.show()

        start_ryu = Excute_ryu(mainwindow) # => excute ryu
        start_ryu.start()

        nodeinfo = MQTT(mainwindow) # => get infomation of node
        nodeinfo.start()
        nodeinfo.dpid_info.connect(mainwindow.loaddata_table_nodeinfo)
        nodeinfo.start_getpacket15.connect(mainwindow.start_getpacket15)
        nodeinfo.start_getpacket05.connect(mainwindow.start_getpacket05)
        
        try:
            sys.exit(app.exec_())
        except:
            SetRule().delete_rule(action='all')
            #AppTable().delete_all()
            print("Exiting")

if __name__ == '__main__':
    text_GUI = Mainapp()