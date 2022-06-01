import sys
from ryu.cmd import manager
from PyQt5.QtCore import QThread


class Excute_ryu(QThread):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        self.main()

    def main(self):
        sys.argv.append('sdn_controller\\start_recive_restful\\ofctl_rest.py')
        #sys.argv.append('--verbose')
        #sys.argv.append('--enable-debugger')
        manager.main()