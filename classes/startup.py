import pandas as pd
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, \
    QApplication, QMainWindow, QStatusBar, QLabel
import sys
import os

configuration_filepath = '../data/configuration-tables.xlsx'


class StartupWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_configuration_tables()

    def init_ui(self):
        self.setWindowTitle('Combat Modeler')
        self.setMinimumSize(800, 600)

        # Add main buttons
        layout = QVBoxLayout()
        show_button = QPushButton("Show Configuration Tables")
        show_button.clicked.connect(self.show_configuration_tables)
        layout.addWidget(show_button)
        start_button = QPushButton("Start Combat")
        start_button.clicked.connect(self.start_combat_window)
        layout.addWidget(start_button)
        self.setLayout(layout)

        # Create status bar.
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

    def load_configuration_tables(self, filepath=configuration_filepath):
        if os.path.exists(filepath):
            # Load Excel sheets into pandas DataFrames
            xls = pd.ExcelFile(filepath)
            required_worksheets = ['Combat Roles', 'Combat Stances', 'Combat Targeting Summary']
            optional_worksheets = ['Combat Role Variations', 'Combat Surges', 'Combat Lulls']
            required_config_dfs = {}
            optional_config_dfs = {}
            for worksheet in required_worksheets:
                try:
                    required_config_dfs[worksheet] = pd.read_excel(xls, worksheet)
                except ValueError:
                    QMessageBox.critical(self, "Error", f"{worksheet} not found in {filepath}")
            print(f"required_config_dfs: {required_config_dfs}")
            config_found_label = QLabel('Config loaded Successfully. ')
            self.statusbar.addWidget(config_found_label)

            for worksheet in optional_worksheets:
                try:
                    optional_config_dfs[worksheet] = pd.read_excel(xls, worksheet)
                    optional_config_loaded_label = QLabel(f'Loaded Optional {worksheet}. ')
                    self.statusbar.addWidget(optional_config_loaded_label)
                except ValueError:
                    optional_config_dfs[worksheet] = None
            print(f"optional_config_dfs: {optional_config_dfs}")

        else:
            config_not_found_label = QLabel('Required Configuration file, configuration-tables.xlsx not found in /data')
            self.statusbar.addWidget(config_not_found_label)

    def show_configuration_tables(self):
        pass

    def start_combat_window(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartupWindow()
    window.show()
    sys.exit(app.exec())
