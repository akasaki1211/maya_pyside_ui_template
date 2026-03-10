#----------------------------------------------
# Simple UI in Maya using PySide.
#----------------------------------------------
from maya import cmds

try: 
    from PySide6 import QtWidgets, QtGui
    from shiboken6 import wrapInstance
    QActionClass = QtGui.QAction
except ImportError:
    from PySide2 import QtWidgets, QtGui
    from shiboken2 import wrapInstance
    QActionClass = QtWidgets.QAction


TITLE = 'My Tool'
VERSION = '1.0.0'


def show_ui():
    from maya import OpenMayaUI
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    maya_main_window = wrapInstance(int(ptr), QtWidgets.QWidget) if ptr else None
    window = UI(parent=maya_main_window)
    window.show()


class UI(QtWidgets.QMainWindow):

    def __init__(self, parent=None, *args, **kwargs):
        super(UI, self).__init__(parent, *args, **kwargs)
        self._init_ui()

    def _init_ui(self, *args):
        self.setWindowTitle(f'{TITLE} {VERSION}')

        # Exit Action
        exit_action = QActionClass("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)

        # About Action
        about_action = QActionClass('About', self)
        about_action.triggered.connect(self._about)

        # Menu Bar
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        help_menu = menu_bar.addMenu("Help")
        help_menu.addAction(about_action)

        # Tool Bar
        tool_bar = self.addToolBar("ToolBar")
        #tool_bar.setMovable(False)
        tool_bar.addAction(exit_action)
        tool_bar.addAction(about_action)

        # Status Bar
        self.statusBar()
        self.statusBar().showMessage('Successfully loaded the tool!')

        # Widgets
        sample_button = QtWidgets.QPushButton("Hello World")
        sample_button.clicked.connect(self._button_clicked)

        # Layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(sample_button)
        
        widget = QtWidgets.QWidget(self)
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def _button_clicked(self, *args):
        message = "Button clicked!"
        color = '#00ffcc'
        size = 20

        cmds.inViewMessage(
            msg=f'<font color={color}>{message}</font>', 
            pos='topCenter', 
            fts=size, 
            fade=True
        )

    def _about(self, *args):
        about_msg = f'{TITLE} {VERSION}\n\n'
        about_msg += 'This is a simple tool built with PySide.\n'
        QtWidgets.QMessageBox.about(self, f'About {TITLE}', about_msg)


if __name__ == '__main__':
    show_ui()