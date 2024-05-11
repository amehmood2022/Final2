import sys
from PyQt6.QtWidgets import QApplication, QDialog
from gui import Ui_Dialog
from logic import BankingLogic
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = QDialog()
    ui = Ui_Dialog()
    ui.setupUi(dialog)
    logic = BankingLogic(ui)
    dialog.show()
    sys.exit(app.exec())