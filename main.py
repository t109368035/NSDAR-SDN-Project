import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from DBControll.NodeTable import NodeTable
from workwidget.main_widget import MainWindow
from sdn_controller.excute_ryu import Excute_ryu
from sdn_controller.SetRule import SetRule
from DBControll.AppTable import AppTable
from DBControll.LinkTable import LinkTable

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
        
        try:
            sys.exit(app.exec_())
        except:
            SetRule().delete_rule(action='all')
            NodeTable().delete_all()
            LinkTable().delete_all()
            #AppTable().delete_all()
            print("Exiting")

if __name__ == '__main__':
    text_GUI = Mainapp()