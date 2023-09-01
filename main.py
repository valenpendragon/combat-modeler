import pandas as pd
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QFileDialog,
                               QMessageBox, QApplication, QMainWindow, QStatusBar,
                               QLabel, QHBoxLayout)
from classes import ConfigurationWindow, CombatModelerWindow
import sys
import os

CONFIGURATION_FILEPATH = './data/configuration-tables.xlsx'
COMBAT_TABLES_FILEPATH = './data/combat-tables.xlsx'
REQUIRED_WORKSHEETS = ['Combat Outcomes', 'Combat Roles', 'Combat Stances',
                       'Combat Targeting Summary']
OPTIONAL_WORKSHEETS = ['Combat Role Variations', 'Combat Surges', 'Combat Lulls']


class StartupWindow(QMainWindow):
    def __init__(self, filepath=CONFIGURATION_FILEPATH):
        super().__init__()
        # Initialize to None the attributes handled by methods:
        # init_ui(), load_configuration_tables(), start_configuration_window()
        # and start_combat_window().
        self.config_path = filepath
        self.vbox = None
        self.statusbar = None
        self.required_config_dfs = None
        self.optional_config_dfs = None
        self.config_window = None
        self.combat_window = None
        self.init_ui()
        self.load_configuration_tables()

    def init_ui(self):
        self.setWindowTitle('Combat Modeler')
        self.setMinimumSize(300, 400)

        # Add main buttons
        show_button = QPushButton("Show Configuration Tables")
        show_button.clicked.connect(self.show_configuration_tables)
        reload_config_button = QPushButton("Reload Configuration Tables")
        reload_config_button.clicked.connect(self.load_configuration_tables)
        start_button = QPushButton("Start Combat")
        start_button.clicked.connect(self.start_combat_window)
        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.exit_app)
        self.setCentralWidget(QWidget(self))
        self.vbox = QVBoxLayout()
        self.centralWidget().setLayout(self.vbox)
        self.vbox.addWidget(show_button)
        self.vbox.addWidget(reload_config_button)
        self.vbox.addWidget(start_button)
        self.vbox.addWidget(exit_button)

        # Create status bar.
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

    def load_configuration_tables(self):
        if os.path.exists(self.config_path):
            # Load Excel sheets into pandas DataFrames
            xls = pd.ExcelFile(self.config_path)
            required_worksheets = REQUIRED_WORKSHEETS
            optional_worksheets = OPTIONAL_WORKSHEETS
            self.required_config_dfs = {}
            self.optional_config_dfs = {}
            for worksheet in required_worksheets:
                try:
                    self.required_config_dfs[worksheet] = pd.read_excel(xls, worksheet)
                except ValueError:
                    QMessageBox.critical(self, "Error", f"Required {worksheet} not found in {self.config_path}")
            print(f"self.required_config_dfs: {self.required_config_dfs}")
            config_found_label = QLabel('Config loaded Successfully. ')
            self.statusbar.addWidget(config_found_label)

            for worksheet in optional_worksheets:
                try:
                    self.optional_config_dfs[worksheet] = pd.read_excel(xls, worksheet)
                    optional_config_loaded_label = QLabel(f'Loaded Optional {worksheet}. ')
                    self.statusbar.addWidget(optional_config_loaded_label)
                except ValueError:
                    self.optional_config_dfs[worksheet] = None
            print(f"optional_config_dfs: {self.optional_config_dfs}")

        else:
            config_not_found_label = QLabel('Required Configuration file, configuration-tables.xlsx not found in /data')
            self.statusbar.addWidget(config_not_found_label)

    def show_configuration_tables(self):
        self.config_window = ConfigurationWindow(self.required_config_dfs,
                                                 self.optional_config_dfs)
        self.config_window.exec()

    def start_combat_window(self):
        self.combat_window = CombatModelerWindow(self.required_config_dfs,
                                                 self.optional_config_dfs)
        self.combat_window.show()

    def exit_app(self):
        sys.exit()


if __name__ == "__main__":
    sys.argv += ['-platform', 'windows:darkmode=2']
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = StartupWindow()
    window.show()
    sys.exit(app.exec())
