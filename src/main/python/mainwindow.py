from PyQt5.QtWidgets import QMainWindow

import traceback, sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

from utils import scraper
class Worker(QRunnable):
    '''Worker thread
    :param fn: The function to be executed
    :param args: Arguments to make available to the run code
    :param kwargs: Keywords arguments to make available to the run code
    '''
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            print("Thread start")
            self.fn(*self.args, self, **self.kwargs)
            print("Thread complete")
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.progress.emit(100) # Done
            

    
class WorkerSignals(QObject):
    '''Defines the signals available from a running worker thread.'''
    error = pyqtSignal(tuple)
    progress = pyqtSignal(int)
    messaging = pyqtSignal(str)


class MainWindow(QMainWindow):
    def __init__(self, ctx, ui, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ctx = ctx # store a reference to the context for resources
        uic.loadUi(ui, self)
        #self.setupUi(self)

        button_action = QAction(
            self.ctx.img_excel, "Download as .csv", self)
        button_action.setStatusTip("Generate CSV file")
        button_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Y))
        button_action.triggered.connect(self.onButtonClick)
        
        self.toCSVButton.setDefaultAction(button_action)
        self.toCSVButton.setToolButtonStyle(Qt.ToolButtonIconOnly)


        self.threadpool = QThreadPool(maxThreadCount=1)
        print("Multithreading with maximum {} threads".format(self.threadpool.maxThreadCount()))


        saveFile = QAction(
            self.ctx.img_folder, "&Save File", self)
        saveFile.setShortcut("Ctrl+S")
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.file_save)
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(saveFile)

        self.SaveTo.setDefaultAction(saveFile)
        self.SaveTo.setToolButtonStyle(Qt.ToolButtonIconOnly)

    def onButtonClick(self, s):
        if not hasattr(self, 'filename'):
            self.need_setup_filename()
        elif not self.threadpool.activeThreadCount():
            companyType = self.CompanyType.text() or ''
            whereTo = self.WhereTo.text() or ''
            filename = self.filename

            worker = Worker(scraper, whereTo, companyType, filename)

            worker.signals.progress.connect(self.update_progress)
            worker.signals.messaging.connect(self.updateStatusBar)
            # Execute
            self.threadpool.start(worker)
        else:     
            self.wait_please()
    
    def update_progress(self, progress):
        self.progressBar.setValue(progress)
    def updateStatusBar(self, string): 
        self.statusbar.showMessage(string)
    
    def wait_please(self):
        dlg = WaitDialog("wait please !", self)
        dlg.exec_()
    
    def need_setup_filename(self):
        dlg = WaitDialog("set up a destination first", self)
        dlg.exec_()

    def file_save(self):
        output_filename, _ = QFileDialog.getSaveFileName(self, 'Save File')
        print( output_filename)
        print( _ )
        self.filename = output_filename
    
class WaitDialog(QDialog):

    def __init__(self, title, *args, **kwargs):
        super(WaitDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle(title)
        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)

        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.buttonBox)  
        self.setLayout(self.layout)
