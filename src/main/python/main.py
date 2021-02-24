from fbs_runtime.application_context.PyQt5 import ApplicationContext, cached_property

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from mainwindow import MainWindow
import sys

class AppContext(ApplicationContext):
    def run(self):
        self.main_window.show()
        return self.app.exec_()

    def get_design(self):
        qtCreatorFile = self.get_resource("gui/mainwindow.ui")
        return qtCreatorFile

    @cached_property
    def main_window(self):
        return MainWindow(self, self.get_design())

    @cached_property
    def img_excel(self):
        return QIcon(self.get_resource('images/excel64.png'))
    
    @cached_property
    def img_folder(self):
        return QIcon(self.get_resource('images/folder.png'))

if __name__ == '__main__':
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)