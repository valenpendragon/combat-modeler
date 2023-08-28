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
    def __init__(self, required_config_dfs, optional_config_dfs, parent=None):
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

        # Create tabs
        self.tab0 = CharacterTab(self)
        self.tab1 = CharacterTab(self)
        self.tab2 = CharacterTab(self)
        self.tab3 = CharacterTab(self)
        self.tab4 = CharacterTab(self)
        self.tab5 = CharacterTab(self)
        self.tab6 = CharacterTab(self)
        self.tab7 = CharacterTab(self)
        self.tab8 = CharacterTab(self)
        self.tab9 = CharacterTab(self)
        self.tab_widget1 = QTabWidget()
        self.tab_widget1.addTab(self.tab0, "One")
        self.tab_widget1.addTab(self.tab1, "Two")
        self.tab_widget1.addTab(self.tab2, "Three")
        self.tab_widget1.addTab(self.tab3, "Four")
        self.tab_widget1.addTab(self.tab4, "Five")
        self.tab_widget2 = QTabWidget()
        self.tab_widget2.addTab(self.tab5, "Six")
        self.tab_widget2.addTab(self.tab6, "Seven")
        self.tab_widget2.addTab(self.tab7, "Eight")
        self.tab_widget2.addTab(self.tab8, "Nine")
        self.tab_widget2.addTab(self.tab9, "Ten")

        mainLayout.addWidget(self.tab_widget1, 0, 0)
        mainLayout.addWidget(self.tab_widget2, 1, 0)

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


class CharacterTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QGridLayout()
        self.tab_name_label = QLabel("Set Tab Name:")
        self.layout.addWidget(self.tab_name_label, 0, 0)
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_input, 0, 1)
        self.setLayout(self.layout)


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
    window = CombatModeler(None, required_config_dfs, optional_config_dfs)
    window.show()
    sys.exit(app.exec())
