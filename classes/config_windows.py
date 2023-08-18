import pandas as pd
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, \
    QApplication, QMainWindow, QStatusBar, QLabel, QHBoxLayout
import sys
import os

CONFIGURATION_FILEPATH = '../data/configuration-tables.xlsx'
REQUIRED_WORKSHEETS = ['Combat Roles', 'Combat Stances', 'Combat Targeting Summary']
OPTIONAL_WORKSHEETS = ['Combat Role Variations', 'Combat Surges', 'Combat Lulls']


class ConfigurationWindow(QMainWindow):
    def __init__(self, required_config_dfs, optional_config_dfs):
        super().__init__()
        self.required_worksheets = REQUIRED_WORKSHEETS
        self.optional_worksheets = OPTIONAL_WORKSHEETS
        self.required_config_dfs = required_config_dfs
        self.optional_config_dfs = optional_config_dfs
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Configuration Data")
        self.setMinimumSize(800, 600)

        # Add show config table buttons.
        # Required config buttons are first.
        combat_role_button = QPushButton("Show Combat Roles")
        combat_role_button.clicked.connect(self.show_combat_roles)
        combat_stances_button = QPushButton("Show Combat Stances")
        combat_stances_button.clicked.connect(self.show_combat_stances)
        combat_targeting_button = QPushButton("Show Combat Targeting Summary")
        combat_targeting_button.clicked.connect(self.show_combat_targeting)
        # Optional buttons are next.
        combat_role_variant_button = QPushButton("Show Combat Role Variations")
        combat_role_variant_button.clicked.connect(self.show_combat_role_variants)
        combat_surges_button = QPushButton("Show Combat Surges")
        combat_surges_button.clicked.connect(self.show_combat_surges)
        combat_lulls_button = QPushButton("Show Combat Lulls")
        combat_lulls_button.clicked.connect(self.show_combat_lulls)
        # Optional configuration tables should be disabled if
        # they are not present.
        if optional_config_dfs["Combat Role Variations"] is None:
            combat_role_variant_button.setEnabled(False)
        if optional_config_dfs["Combat Surges"] is None:
            combat_surges_button.setEnabled(False)
        if optional_config_dfs["Combat Lulls"] is None:
            combat_lulls_button.setEnabled(False)
        # Put all six buttons in the status bar.
        self.statusbar = QStatusBar()
        self.statusbar.addWidget(combat_role_button)
        self.statusbar.addWidget(combat_stances_button)
        self.statusbar.addWidget(combat_targeting_button)
        self.statusbar.addWidget(combat_role_variant_button)
        self.statusbar.addWidget(combat_surges_button)
        self.statusbar.addWidget(combat_lulls_button)
        self.setStatusBar(self.statusbar)


    def show_combat_roles(self):
        pass

    def show_combat_stances(self):
        pass

    def show_combat_targeting(self):
        pass

    def show_combat_role_variants(self):
        pass

    def show_combat_surges(self):
        pass

    def show_combat_lulls(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    required_config_dfs = {}
    optional_config_dfs = {}
    xls = pd.ExcelFile(CONFIGURATION_FILEPATH)
    for worksheet in REQUIRED_WORKSHEETS:
        required_config_dfs[worksheet] = pd.read_excel(xls, worksheet)
    for worksheet in OPTIONAL_WORKSHEETS:
        optional_config_dfs[worksheet] = pd.read_excel(xls, worksheet)
    window = ConfigurationWindow(required_config_dfs, optional_config_dfs)
    window.show()
    sys.exit(app.exec())
