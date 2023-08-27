import pandas as pd
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, \
    QApplication, QMainWindow, QStatusBar, QLabel, QHBoxLayout, QDialog, QTableView, \
    QGridLayout, QDialogButtonBox, QTabWidget, QLineEdit, QTextEdit
from entities import PandasModel
import sys
import os

CONFIGURATION_FILEPATH = '../data/configuration-tables.xlsx'
REQUIRED_WORKSHEETS = ['Combat Roles', 'Combat Stances', 'Combat Targeting Summary']
OPTIONAL_WORKSHEETS = ['Combat Role Variations', 'Combat Surges', 'Combat Lulls']
DIFFICULTY_VARIATIONS = ['A', 'B', 'C', 'D']
INDIVIDUAL_LEVEL = ['Low', 'Moderate', 'Advanced', 'Elite']


class CombatModeler(QWidget):
    def __init__(self, parent, required_config_dfs, optional_config_dfs):
        super().__init__(parent)
        self.setMinimumSize(800, 600)
        self.setWindowTitle("Combat Modeler")

        mainLayout = QGridLayout()

        # We need lists made from the first column of each config dataframe.
        self.config = self.extract_dropdown_lists(required_config_dfs,
                                                  optional_config_dfs)
        # We also need the actual dataframes for combat surges and lulls, either
        # as None or as a dataframe.
        self.combat_surges = optional_config_dfs['Combat Surges']
        self.combat_lulls = optional_config_dfs['Combat Lulls']
        print(f"config: {self.config}")
        print(f"combat_surges: {self.combat_surges}")
        print(f"combat_lulls: {self.combat_lulls}")

        self.tab1 = QWidget()
        self.tab1.layout = QGridLayout()
        self.tab1.tab_name_label = QLabel("Set Tab Name:")
        self.tab1.layout.addWidget(self.tab1.tab_name_label, 0, 0)
        self.tab1.name_input = QLineEdit()
        self.tab1.layout.addWidget(self.tab1.name_input, 0, 1)
        self.tab1.setLayout(self.tab1.layout)

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.tab1, "One")

        mainLayout.addWidget(self.tab_widget, 0, 0)

        # Build text display area here.
        self.text_display = QTextEdit(self)
        self.text_display.setReadOnly(True)

        mainLayout.addWidget(self.text_display, 0, 1)

        self.setLayout(mainLayout)

    def extract_dropdown_lists(self, required_config_dfs, optional_config_dfs):
        """
        This method requires two dictionaries of dataframes. Elements of the optional
        configs will be None. From both dictionaries, it will extract a dictionary of
        lists of options for the CombatModeler dropdown boxes.
        :param required_config_dfs: dict of pd.DataFrame
        :param optional_config_dfs: dict of pd.DataFrame
        :return: dict of list
        """
        config = {}
        for worksheet in REQUIRED_WORKSHEETS:
            df = required_config_dfs[worksheet]
            col_list = df[df.columns[0]].values.tolist()
            config[worksheet] = col_list
        if optional_config_dfs['Combat Role Variations'] is not None:
            df = optional_config_dfs['Combat Role Variations']
            col_list = df[df.columns[0]].values.tolist()
            config['Combat Role Variations'] = col_list
        else:
            config['Combat Role Variations'] = None
        if (optional_config_dfs['Combat Surges'] is not None) or\
            (optional_config_dfs['Combat Lulls'] is not None):
            config['Surges and Lulls'] = INDIVIDUAL_LEVEL
        else:
            config['Surges and Lulls'] = None
        config['Relative Difficulty'] = DIFFICULTY_VARIATIONS
        return config


if __name__ == "__main__":
    app = QApplication(sys.argv)
    required_config_dfs = {}
    optional_config_dfs = {}
    xls = pd.ExcelFile(CONFIGURATION_FILEPATH)
    for worksheet in REQUIRED_WORKSHEETS:
        required_config_dfs[worksheet] = pd.read_excel(xls, worksheet)
    for worksheet in OPTIONAL_WORKSHEETS:
        optional_config_dfs[worksheet] = pd.read_excel(xls, worksheet)
    window = CombatModeler(None, required_config_dfs, optional_config_dfs)
    window.show()
    sys.exit(app.exec())
