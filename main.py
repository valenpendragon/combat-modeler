import pandas as pd
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QFileDialog,
                               QMessageBox, QApplication, QMainWindow, QStatusBar,
                               QLabel, QHBoxLayout)
from classes import ConfigurationWindow, CombatModelerWindow
import sys
import os

CONFIGURATION_FILEPATH = 'data/configuration-tables.xlsx'
COMBAT_TABLES_FILEPATH = 'data/combat-tables.xlsx'
REQUIRED_WORKSHEETS = ['Combat Outcomes', 'Combat Roles', 'Combat Stances',
                       'Combat Targeting Summary']
OPTIONAL_WORKSHEETS = ['Combat Role Variations', 'Combat Surges', 'Combat Lulls']
DIFFICULTY_VARIATIONS = ['A', 'B', 'C', 'D']
INDIVIDUAL_LEVEL = ['Low', 'Moderate', 'Advanced', 'Elite']


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
        self.validate_tables()

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
            QMessageBox.critical(self, 'Fatal Error',
                                 'Required Configuration file, configuration-tables.xlsx not found in /data')

    def validate_tables(self):
        # One error is enough to stop this software from working properly.
        # str.strip() is used to reduce the impact of typos in header columns.
        for title in self.required_config_dfs.keys():
            errors = 0
            worksheet = self.required_config_dfs[title]
            if len(worksheet.columns) != 2:
                errors += 1
            if worksheet.columns[1].strip() != 'Description':
                errors += 1
            if title == "Combat Outcomes" or title == "Combat Targeting Summary":
                if worksheet.columns[0].strip() != 'Outcome':
                    errors += 1
            elif title == "Combat Roles" or title == "Combat Stances":
                if worksheet.columns[0].strip() != 'Role':
                    errors += 1
            else:
                # There is an extra table loaded that is not required.
                errors += 1
            for col in worksheet.columns:
                for idx in worksheet.index:
                    if not isinstance(worksheet[col][idx], str):
                        errors += 1
            if errors > 0:
                error_msg = f"Format of required configuration worksheet, {title}, is invalid."
                QMessageBox.critical(self, 'Fatal Error', error_msg)

        for title in self.optional_config_dfs.keys():
            errors = 0
            if self.optional_config_dfs[title] is None:
                continue
            else:
                worksheet = self.optional_config_dfs[title]
                if title == "Combat Role Variations":
                    if len(worksheet.columns) != 2:
                        errors += 1
                    else:
                        df_cols = [col.strip() for col in worksheet.columns]
                        if df_cols != ['Role Variant', 'Description']:
                            errors += 1
                    for col in worksheet.columns:
                        for idx in worksheet.index:
                            if not isinstance(worksheet[col][idx], str):
                                errors += 1
                else:
                    # This is either a Combat Surges or Lulls table.
                    # Construct the list of columns.
                    cols = ['Outcome']
                    min_lvls = [f"Minor {level}" for level in INDIVIDUAL_LEVEL]
                    maj_lvls = [f"Major {level}" for level in INDIVIDUAL_LEVEL]
                    cols.extend(min_lvls)
                    cols.extend(maj_lvls)
                    df_cols = [col.strip() for col in worksheet.columns]
                    if cols != df_cols:
                        errors += 1
                    for col in worksheet.columns:
                        for idx in worksheet.index:
                            if not isinstance(worksheet[col][idx], str):
                                errors += 1
            if errors > 0:
                error_msg = f"Format of optional configuration worksheet, {title}, is invalid."
                QMessageBox.critical(self, 'Fatal Error', error_msg)

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
