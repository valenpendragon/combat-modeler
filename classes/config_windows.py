import pandas as pd
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, \
    QApplication, QMainWindow, QStatusBar, QLabel, QHBoxLayout, QDialog
import sys
import os

CONFIGURATION_FILEPATH = '../data/configuration-tables.xlsx'
REQUIRED_WORKSHEETS = ['Combat Roles', 'Combat Stances', 'Combat Targeting Summary']
OPTIONAL_WORKSHEETS = ['Combat Role Variations', 'Combat Surges', 'Combat Lulls']


class ConfigurationWindow(QDialog):
    def __init__(self, required_config_dfs, optional_config_dfs):
        super().__init__()
        self.required_worksheets = REQUIRED_WORKSHEETS
        self.optional_worksheets = OPTIONAL_WORKSHEETS
        self.required_config_dfs = required_config_dfs
        self.optional_config_dfs = optional_config_dfs
        self.setWindowTitle("Configuration Data")

        # Add show config table buttons.
        # Required config buttons are first.
        self.combat_role_button = QPushButton("Show Combat Roles")
        self.combat_role_button.clicked.connect(self.show_combat_roles)
        self.combat_stances_button = QPushButton("Show Combat Stances")
        self.combat_stances_button.clicked.connect(self.show_combat_stances)
        self.combat_targeting_button = QPushButton("Show Combat Targeting Summary")
        self.combat_targeting_button.clicked.connect(self.show_combat_targeting)
        # Optional buttons are next.
        self.combat_role_variant_button = QPushButton("Show Combat Role Variations")
        self.combat_role_variant_button.clicked.connect(self.show_combat_role_variants)
        self.combat_surges_button = QPushButton("Show Combat Surges")
        self.combat_surges_button.clicked.connect(self.show_combat_surges)
        self.combat_lulls_button = QPushButton("Show Combat Lulls")
        self.combat_lulls_button.clicked.connect(self.show_combat_lulls)
        # Optional configuration tables should be disabled if
        # they are not present.
        if optional_config_dfs["Combat Role Variations"] is None:
            self.combat_role_variant_button.setEnabled(False)
        if optional_config_dfs["Combat Surges"] is None:
            self.combat_surges_button.setEnabled(False)
        if optional_config_dfs["Combat Lulls"] is None:
            self.combat_lulls_button.setEnabled(False)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.combat_role_button)
        self.layout.addWidget(self.combat_stances_button)
        self.layout.addWidget(self.combat_targeting_button)
        self.layout.addWidget(self.combat_role_variant_button)
        self.layout.addWidget(self.combat_surges_button)
        self.layout.addWidget(self.combat_lulls_button)

    def show_combat_roles(self):
        print(f"Combat Roles button pressed.")

    def show_combat_stances(self):
        print(f"Combat Stances button pressed.")

    def show_combat_targeting(self):
        print(f"Combat Targeting button pressed.")

    def show_combat_role_variants(self):
        print(f"Combat Role Variants button pressed.")

    def show_combat_surges(self):
        print(f"Combat Surges button pressed.")

    def show_combat_lulls(self):
        print(f"Combat Lulls button pressed.")


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
