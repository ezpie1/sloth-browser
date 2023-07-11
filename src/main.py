import sys

from mainWindow import MainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Sloth")
    app.setWindowIcon(QIcon("assets/logo/icon.png"))

    window = MainWindow()
    
    app.setStyleSheet("""
    QWidget#SideBar {
        background-color: #808080;
    }

    QToolBar {
        background-color: #808080;
    }

    QListView {
    background-color: #808080;
    color: #ffffff;
    font-size: 20px;
    }

    QToolButton {
    background-color: transparent;
    }

    QLineEdit {
        height: 25px;
        border-radius: 10px;
        padding-left: 10px;
        padding-right: 10px;
        margin-left: 20px;
        margin-right: 20px;
    }
    """)

    sys.exit(app.exec_())
