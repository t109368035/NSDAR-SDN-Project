import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from workwidget.main_widget import MainWindow
from get_user.get_packet import Remote_capture
from sdn_controller.excute_ryu import Excute_ryu
from node_info.mqtt_subscriber import MQTT_Subscriber
from sdn_controller.innitial import innitial_rule

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
        start_ryu.serve()
        innitial_rule() # => comfirm all ovs connected with controller, let each node can ping each other(same channel)

        getUser = Remote_capture(mainwindow) # => capture user_data 
        #getUser.setDaemon(True)
        getUser.serve()
        getUser.map15_user.connect(mainwindow.loaddata) # => throw user_data to ui

        mqttService = MQTT_Subscriber(mainwindow) # => revive ETX
        mqttService.serve()

        try:
            sys.exit(app.exec_())
        except:
            print("Exiting")

if __name__ == '__main__':
    text_GUI = Mainapp()