#----------------------------------------------
# Custom Modal Dialog in Maya using PySide.
#----------------------------------------------
try:
    from PySide6 import QtWidgets
except ImportError:
    from PySide2 import QtWidgets


TITLE = 'My Custom Dialog'


class BaseDialog(QtWidgets.QDialog):
    
    def __init__(self, parent=None, title: str = "Custom Dialog", *args, **kwargs):
        super(BaseDialog, self).__init__(parent, *args, **kwargs)
        self.setWindowTitle(title)

    def add_buttons(self, ok_text: str = "OK", cancel_text: str = "Cancel") -> QtWidgets.QDialogButtonBox:
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        button_box.button(QtWidgets.QDialogButtonBox.Ok).setText(ok_text)
        button_box.button(QtWidgets.QDialogButtonBox.Cancel).setText(cancel_text)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        return button_box


class InputDialog(BaseDialog):

    def __init__(self, parent=None, *args, **kwargs) -> None:
        super(InputDialog, self).__init__(parent, title=TITLE, *args, **kwargs)
        self._init_ui()

    def _init_ui(self):
        self.resize(300, 50)

        # Widgets
        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.setPlaceholderText("Enter text here...")
        button_box = self.add_buttons(ok_text="OK", cancel_text="Cancel")

        # Layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.line_edit)
        main_layout.addWidget(button_box)

        self.setLayout(main_layout)

    def _get_text(self):
        return self.line_edit.text()

    @staticmethod
    def get_input(parent=None) -> str:
        dialog = InputDialog(parent)
        result = dialog.exec()

        if result == QtWidgets.QDialog.Accepted:
            return dialog._get_text()
        return None


if __name__ == '__main__':
    text = InputDialog.get_input(parent=None)
    if text:
        print("Input:", text)