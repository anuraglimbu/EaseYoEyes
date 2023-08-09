from color_api import *

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class About(QMainWindow):
    def __init__(self, parent=None):
        super(About, self).__init__(parent)

        self.setWindowTitle("About")
        self.setFixedSize(300, 200)
        self.setWindowIcon(QIcon(QIcon("resources/icon.ico")))
        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & Qt.WindowCloseButtonHint)

        self.logo = QLabel()
        pixmap = QPixmap('resources/icon.ico')
        self.logo.setPixmap(pixmap)

        self.label = QLabel(str("EaseYoEyes"))
        self.label.setFont(QFont("Calibri", 15, QFont.Bold))

        self.ver = QLabel(str("version 0.5"))
        self.ver.setFont(QFont("Calibri", 12, QFont.Bold))

        self.cr = QLabel(str("- Anurag Limbu"))
        self.cr.setFont(QFont("Calibri", 9, QFont.Bold))

        self.grid = QGridLayout()
        self.grid.addWidget(self.logo, 0, 0)
        self.grid.addWidget(self.label, 0, 1)
        self.grid.addWidget(self.ver, 1,1)
        self.grid.addWidget(self.cr, 2, 1)

        self.wid = QWidget(self)
        self.setCentralWidget(self.wid)
        self.wid.setLayout(self.grid)

    def closeEvent(self, event):
        event.ignore()
        self.hide()

class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.first = 1
        
        icon = QIcon("resources/icon.bmp")

        self.setWindowTitle("EaseYoEyes")
        self.setFixedSize(850, 450)
        self.setWindowIcon(QIcon(icon))
        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & Qt.WindowCloseButtonHint)

        self.about = About()

        slider_css = """
            QSlider::groove:horizontal { 
                background-color: #30a1d9;
                border: 0px solid #30a1d9; 
                height: 10px; 
                border-radius: 4px;
            }

            QSlider::handle:horizontal { 
                background-color: #e3e3e3; 
                border: 2px solid #b4b1b1; 
                width: 16px; 
                height: 20px;
                line-height: 20px; 
                margin-top: -5px; 
                margin-bottom: -5px; 
                border-radius: 10px; 
            }

            QSlider::handle:horizontal:hover { 
                border-radius: 10px;
            }
        """

        menubtn_css = """
            QPushButton {
                height = 50px;
                color: red; 
                background-color: white; 
            }
        """

        title_font = """
            QLabel{
                color : #30a1d9;
            }

            QLabel:hover { 
                color : #006644;
            }
        """

        self.menubtn = QPushButton()
        self.menubtn.setIcon(QIcon("resources/menu.ico"))
        self.menubtn.setStyleSheet(menubtn_css)

        self.label = QLabel(str("Ease the color temperature as it suits to your eyes!"))
        self.label.setFont(QFont("Calibri", 17, QFont.Bold))
        self.label.setStyleSheet(title_font)

        self.warm_slider = QSlider(Qt.Horizontal)
        self.warm_slider.setFocusPolicy(Qt.StrongFocus)
        self.warm_slider.setMaximum(100)
        self.warm_slider.setMinimum(0)
        self.warm_slider.setSingleStep(1)
        self.warm_slider.setValue(100)
        self.warm_slider.valueChanged.connect(self.update)
        self.warm_slider.setStyleSheet(slider_css)

        self.labelWarm = QLabel(str("Warmer"))
        self.labelWarm.setFont(QFont("Calibri", 13, QFont.Bold))
        self.labelCold = QLabel(str("Brighter"))
        self.labelCold.setFont(QFont("Calibri", 13, QFont.Bold))

        
        self.grid = QGridLayout()
        self.grid.addWidget(self.menubtn, 0, 0)
        self.grid.addWidget(self.label, 0, 1)
        self.grid.addWidget(self.labelWarm, 4, 0)
        self.grid.addWidget(self.warm_slider, 4, 1)
        self.grid.addWidget(self.labelCold, 4, 2)

        self.setLayout(self.grid)

        # Create the tray
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(icon)
        self.tray.setVisible(True)
        self.tray.setToolTip("EaseYoEyes")

        self.tray.activated.connect(self.__icon_activated)

        # Create the menu
        self.menu = QMenu()
        self.action1 = QAction("EaseYoEyes")
        self.action1.setFont(QFont("Calibri", 10, QFont.Bold))
        self.action1.triggered.connect(self.show_win)
        self.menu.addAction(self.action1)

        self.action2 = QAction("About EaseYoEyes")
        self.action2.triggered.connect(self.show_about)
        self.menu.addAction(self.action2)

        self.menu.addSeparator()

        self.action3 = QAction("Exit EaseYoEyes (v0.5)")
        self.action3.triggered.connect(self.exit)
        self.menu.addAction(self.action3)

        # Add the menu to the tray
        self.tray.setContextMenu(self.menu)
        self.menubtn.setMenu(self.menu)

        #self.statusBar().showMessage("-By Ordinary Guy")

    def exit(self):
        self.tray.hide()
        qApp.quit()

    def show_win(self):
        self.show()

    def show_about(self):
        self.about.show()

    def notify(self, message):
        if self.first == 1: 
            self.tray.showMessage("EaseYoEyes", message, QSystemTrayIcon.Information, 3000)
            self.first = 2

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.notify("App has been minimized to system tray")
    
    def __icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()

    def place_initial_screen(self):
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()

        widget = self.geometry()
        x = (ag.width() - widget.width()) - 10
        y = (2 * ag.height() - sg.height() - widget.height()) - 50
        self.move(x, y)

    def update(self):
        wr = ctypes.c_float
        wr = float(self.warm_slider.value())
        SetWarmth(wr)

app = QApplication(sys.argv)
widget = Window()
widget.place_initial_screen()
widget.show()
sys.exit(app.exec_())

Reset()
