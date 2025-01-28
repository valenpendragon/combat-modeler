import pandas as pd
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QFileDialog,
                               QMessageBox, QApplication, QMainWindow, QStatusBar,
                               QLabel, QHBoxLayout)
from classes import ConfigurationWindow, CombatModelerWindow
import sys
import os

CONFIGURATION_FILEPATH = 'data_orig/configuration-tables.xlsx'
COMBAT_TABLES_FILEPATH = 'data_orig/combat-tables.xlsx'
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
                    QMessageBox.critical(self, "Error", f"Required {worksheet} not found in"
                                                        f" {self.config_path}")
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
                                 'Required Configuration file, configuration-tables.xlsx not '
                                 'found in /data')

    def validate_tables(self):
        # One error is enough to stop this software from working properly.
        # str.strip() is used to reduce the impact of typos in header columns.
        for title in self.required_config_dfs.keys():
            errors = 0
            worksheet = self.required_config_dfs[title]
            if len(worksheet.columns) != 2:
                errors += 1
                print(f"StartupWindow.validate_tables: Required {title} has the wrong "
                      f"number of columns.")
            if worksheet.columns[1].strip() != 'Description':
                errors += 1
                print(f"StartupWindow.validate_tables: Required {title} is missing "
                      f"'Description' column.")
            if title == "Combat Outcomes" or title == "Combat Targeting Summary":
                if worksheet.columns[0].strip() != 'Outcome':
                    errors += 1
                    print(f"StartupWindow.validate_tables: Required {title} is missing "
                          f"'Outcome' column.")
            elif title == "Combat Roles" or title == "Combat Stances":
                if worksheet.columns[0].strip() != 'Role':
                    errors += 1
                    print(f"StartupWindow.validate_tables: Required {title} is missing "
                          f"'Role' column.")
            else:
                # There is an extra table loaded that is not required.
                errors += 1
                print(f"StartupWindow.validate_tables: {title} in required tables "
                      f"is extraneous.")
            for col in worksheet.columns:
                for idx in worksheet.index:
                    if not isinstance(worksheet[col][idx], str):
                        errors += 1
                        print(f"StartupWindow.validate_tables: Required {title} has column "
                              f"{worksheet[col][idx]} that is not a string.")
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
                        print(f"StartupWindow.validate_tables: Optional {title} has the wrong "
                              f"number of columns.")
                    else:
                        df_cols = [col.strip() for col in worksheet.columns]
                        if df_cols != ['Role Variant', 'Description']:
                            errors += 1
                            print(f"StartupWindow.validate_tables: Optional {title} has "
                                  f"incorrect columns {df_cols}.")
                    for col in worksheet.columns:
                        for idx in worksheet.index:
                            if not isinstance(worksheet[col][idx], str):
                                errors += 1
                                print(f"StartupWindow.validate_tables: Optional {title} has "
                                      f"column {worksheet[col][idx]} that is not a string.")
                else:
                    # This is either a Combat Surges or Lulls table.
                    # Construct the list of columns.
                    cols = ['Outcome']
                    min_lvls = [f"Minor {level}" for level in INDIVIDUAL_LEVEL]
                    print(f"StartupWindow.validate_tables: min_lvls: {min_lvls}.")
                    maj_lvls = [f"Major {level}" for level in INDIVIDUAL_LEVEL]
                    print(f"StartupWindow.validate_tables: maj_lvls: {maj_lvls}.")
                    cols.extend(min_lvls)
                    cols.extend(maj_lvls)
                    print(f"StartupWindow.validate_tables: cols: {cols}")
                    df_cols = [col.strip() for col in worksheet.columns]
                    print(f"StartupWindow.validate_tables: df_cols: {df_cols}")
                    if cols != df_cols:
                        errors += 1
                        print(f"StartupWindow.validate_tables: cols and df_cols are not "
                              f"equal in Combat Surge/Lull table {title}")
                    for col in worksheet.columns:
                        for idx in worksheet.index:
                            if not isinstance(worksheet[col][idx], str):
                                errors += 1
                                print(f"StartupWindow.validate_tables: Combat Surge/Lull "
                                      f"table {title} has a column {worksheet[col][idx]} "
                                      f"that is not a string.")
            if errors > 0:
                error_msg = f"Format of optional configuration worksheet, {title}, is invalid."
                QMessageBox.critical(self, 'Fatal Error', error_msg)

    def show_configuration_tables(self):
        self.config_window = ConfigurationWindow(self.required_config_dfs,
                                                 self.optional_config_dfs)
        self.config_window.exec()

    def start_combat_window(self):
        self.combat_window = CombatModelerWindow(self.required_config_dfs,
                                                 self.optional_config_dfs,
                                                 COMBAT_TABLES_FILEPATH)
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
