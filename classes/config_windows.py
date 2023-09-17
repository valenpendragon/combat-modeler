import pandas as pd
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, \
    QApplication, QMainWindow, QStatusBar, QLabel, QHBoxLayout, QDialog, QTableView, \
    QGridLayout, QDialogButtonBox
from entities import PandasModel
import sys
import os

CONFIGURATION_FILEPATH = '../data/configuration-tables.xlsx'
REQUIRED_WORKSHEETS = ['Combat Outcomes', 'Combat Roles', 'Combat Stances',
                       'Combat Targeting Summary']
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
        self.combat_outcome_button = QPushButton("Show Combat Outcomes")
        self.combat_outcome_button.clicked.connect(self.show_combat_outcomes)
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
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        # Optional configuration tables should be disabled if
        # they are not present.
        if optional_config_dfs["Combat Role Variations"] is None:
            self.combat_role_variant_button.setEnabled(False)
        if optional_config_dfs["Combat Surges"] is None:
            self.combat_surges_button.setEnabled(False)
        if optional_config_dfs["Combat Lulls"] is None:
            self.combat_lulls_button.setEnabled(False)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.combat_outcome_button)
        self.layout.addWidget(self.combat_role_button)
        self.layout.addWidget(self.combat_stances_button)
        self.layout.addWidget(self.combat_targeting_button)
        self.layout.addWidget(self.combat_role_variant_button)
        self.layout.addWidget(self.combat_surges_button)
        self.layout.addWidget(self.combat_lulls_button)
        self.layout.addWidget(self.close_button)

    def show_required_combat_data(self, title):
        data = self.required_config_dfs[title]
        print(f"data_orig: {data}")
        dialog = ConfigDisplayDialog(title, data)
        dialog.exec()

    def show_optional_combat_data(self, title):
        data = self.optional_config_dfs[title]
        print(f"data_orig: {data}")
        if data is None:
            dialog = QMessageBox()
            dialog.setText(f"{title} is not configured in the files in data_orig.")
            dialog.setWindowTitle("Configuration does not exist")
            dialog.setStandardButtons(QMessageBox.Cancel)
            dialog.exec()
        else:
            dialog = ConfigDisplayDialog(title, data)
            dialog.exec()

    def show_combat_outcomes(self):
        self.show_required_combat_data("Combat Outcomes")

    def show_combat_roles(self):
        self.show_required_combat_data("Combat Roles")

    def show_combat_stances(self):
        self.show_required_combat_data("Combat Stances")

    def show_combat_targeting(self):
        self.show_required_combat_data("Combat Targeting Summary")

    def show_combat_role_variants(self):
        self.show_optional_combat_data("Combat Role Variations")

    def show_combat_surges(self):
        self.show_optional_combat_data("Combat Surges")

    def show_combat_lulls(self):
        self.show_optional_combat_data("Combat Lulls")


class ConfigDisplayDialog(QDialog):
    def __init__(self, window_title: str, data: pd.DataFrame):
        super().__init__()
        self.setWindowTitle(window_title)
        self.setMinimumSize(800, 400)
        layout = QVBoxLayout()
        self.view = QTableView()
        self.view.horizontalHeader().setStretchLastSection(True)
        self.view.setAlternatingRowColors(True)
        self.view.setSelectionBehavior(QTableView.SelectRows)
        self.model = PandasModel(data)
        self.view.setModel(self.model)
        layout.addWidget(self.view)
        self.buttonbox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)
        layout.addWidget(self.buttonbox)
        self.setLayout(layout)


if __name__ == "__main__":
    sys.argv += ['-platform', 'windows:darkmode=2']
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    required_config_dfs = {}
    optional_config_dfs = {}
    xls = pd.ExcelFile(CONFIGURATION_FILEPATH)
    for worksheet in REQUIRED_WORKSHEETS:
        required_config_dfs[worksheet] = pd.read_excel(xls, worksheet)
    for worksheet in OPTIONAL_WORKSHEETS:
        optional_config_dfs[worksheet] = pd.read_excel(xls, worksheet)
    print(f"required config dfs: {required_config_dfs}")
    print(f"optional config dfs: {optional_config_dfs}")
    window = ConfigurationWindow(required_config_dfs, optional_config_dfs)
    window.show()
    sys.exit(app.exec())
