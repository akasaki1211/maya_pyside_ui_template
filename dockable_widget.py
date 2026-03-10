#----------------------------------------------
# Dockable widget in Maya using PySide.
# 
# Place this file in PYTHONPATH and execute the following code in Maya:
#   import dockable_widget
#   dockable_widget.show_ui()
#----------------------------------------------

from maya import cmds, OpenMayaUI

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

MODULE_NAME = "dockable_widget" # module name for uiScript.
OBJECT_NAME = "MyToolWindow"
WORKSPACE_CONTROL = f"{OBJECT_NAME}WorkspaceControl"
UI_SCRIPT = f"import {MODULE_NAME} as _m\n_m.restore()"


def show_ui():
    from maya import OpenMayaUI
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    maya_main_window = wrapInstance(int(ptr), QtWidgets.QWidget) if ptr else None
    window = UI(parent=maya_main_window)
    window.show()


def show_ui():
    if cmds.workspaceControl(WORKSPACE_CONTROL, exists=True):
        cmds.workspaceControl(WORKSPACE_CONTROL, e=True, restore=True)
    else:
        cmds.workspaceControl(
            WORKSPACE_CONTROL,
            label=f"{TITLE} {VERSION}",
            uiScript=UI_SCRIPT,
            retain=True,
            loadImmediately=True,
        )

    restore()


_window = None

def restore(*_args):

    global _window

    # call by uiScript()
    ptr = OpenMayaUI.MQtUtil.getCurrentParent()
    if not ptr:
        # call by show_ui()
        ptr = OpenMayaUI.MQtUtil.findControl(WORKSPACE_CONTROL)

    host = wrapInstance(int(ptr), QtWidgets.QWidget) if ptr else None
    if host is None:
        return

    # delete old instance of UI if exists
    for child in host.findChildren(QtWidgets.QWidget):
        if child.objectName() == OBJECT_NAME:
            child.setParent(None)
            child.deleteLater()

    _window = UI(parent=host)
    host.layout().addWidget(_window)
    _window.show()


class UI(QtWidgets.QWidget):

    def __init__(self, parent=None, *args, **kwargs):
        super(UI, self).__init__(parent, *args, **kwargs)
        self.setObjectName(OBJECT_NAME)
        self._init_ui()

    def _init_ui(self, *args):
        self.setWindowTitle(f'{TITLE} {VERSION}')

        # Widgets
        sample_button = QtWidgets.QPushButton("Hello World")
        sample_button.clicked.connect(self._button_clicked)
        
        # Layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(sample_button)
    
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
