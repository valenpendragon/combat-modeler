import pandas as pd
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QFileDialog,
                               QMessageBox, QApplication, QMainWindow, QStatusBar,
                               QLabel, QHBoxLayout, QDialog, QTableView,
                               QGridLayout, QDialogButtonBox, QTabWidget,
                               QLineEdit, QTextEdit, QComboBox, QToolBar, QToolButton)
from entities import PandasModel, Character
import sys
import os

CONFIGURATION_FILEPATH = '../data/configuration-tables.xlsx'
REQUIRED_WORKSHEETS = ['Combat Outcomes', 'Combat Roles', 'Combat Stances',
                       'Combat Targeting Summary']
OPTIONAL_WORKSHEETS = ['Combat Role Variations', 'Combat Surges', 'Combat Lulls']
DIFFICULTY_VARIATIONS = ['A', 'B', 'C', 'D']
INDIVIDUAL_LEVEL = ['Low', 'Moderate', 'Advanced', 'Elite']


class CombatModelerWindow(QWidget):
    def __init__(self, required_config_dfs, optional_config_dfs, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 600)
        self.setWindowTitle("Combat Modeler")
        self.combat_action_abbrev = None

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
        self.create_combat_action_abbrev()

        # Create tabs
        self.tab0 = CharacterTab(self, self.config, "One")
        self.tab1 = CharacterTab(self, self.config, "Two")
        self.tab2 = CharacterTab(self, self.config, "Three")
        self.tab3 = CharacterTab(self, self.config, "Four")
        self.tab4 = CharacterTab(self, self.config, "Five")
        self.tab5 = CharacterTab(self, self.config, "Six")
        self.tab6 = CharacterTab(self, self.config, "Seven")
        self.tab7 = CharacterTab(self, self.config, "Eight")
        self.tab8 = CharacterTab(self, self.config, "Nine")
        self.tab9 = CharacterTab(self, self.config, "Ten")
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

        mainLayout.addWidget(self.text_display, 0, 1, 0, 1)

        # Adding Toolbar.
        self.toolbar = QToolBar()
        self.run_sim_button = QPushButton("Run Simulation")
        self.run_sim_button.clicked.connect(self.run_simulation)
        self.toolbar.addWidget(self.run_sim_button)
        self.save_tab_data_button = QPushButton("Save Tab Data")
        self.save_tab_data_button.clicked.connect(self.save_tab_data)
        self.toolbar.addWidget(self.save_tab_data_button)
        self.clear_tab_data_button = QPushButton("Clear Tab Data")
        self.save_tab_data_button.clicked.connect(self.clear_tabs)
        self.toolbar.addWidget(self.clear_tab_data_button)
        self.close_window_button = QPushButton("Close Window")
        self.close_window_button.clicked.connect(self.close_simulator)
        self.toolbar.addWidget(self.close_window_button)

        mainLayout.addWidget(self.toolbar, 2, 0, 3, 0)

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

    def run_simulation(self):
        pass

    def clear_tabs(self):
        pass

    def save_tab_data(self):
        pass

    def close_simulator(self):
        self.close()

    def create_combat_action_abbrev(self):
        """This method extracts the abbreviation from Combat Outcomes so
        they can be displayed properly in the combat text feed."""
        abbrev = []
        data = self.config["Combat Outcomes"]
        for item in data:
            title = item.split(' ')
            s = ''
            if title == 1:
                abbrev.append(item[0:2].upper())
            else:
                for word in title:
                    s += word[0]
                abbrev.append(s)
        self.combat_action_abbrev = abbrev


class CharacterTab(QWidget):
    def __init__(self, parent, config, name):
        super().__init__(parent)
        self.config = config

        # Create character assigned to this tab.
        default_name = name
        default_combat_role = config['Combat Roles'][0]
        default_combat_stance = config['Combat Stances'][0]
        default_difficulty = config['Relative Difficulty'][0]
        if config['Combat Role Variations'] is not None:
            default_role_variant = config['Combat Role Variations'][0]
        else:
            default_role_variant = None
        if config['Surges and Lulls'] is not None:
            default_level = INDIVIDUAL_LEVEL[0]
        else:
            default_level = None
        self.character = Character(name = default_name,
                                   combat_role=default_combat_role,
                                   combat_stance=default_combat_stance,
                                   difficulty=default_difficulty,
                                   role_variant=default_role_variant,
                                   individual_level=default_level)

        # Set up tab layout and widget content.
        self.layout = QGridLayout()
        self.tab_name_label = QLabel("Set Name:")
        self.layout.addWidget(self.tab_name_label, 0, 0)
        self.name_input = QLineEdit(self)
        self.name_input.setText(default_name)
        self.layout.addWidget(self.name_input, 0, 1)

        # Create Combat Role ComboBox.
        self.combat_role_label = QLabel("Combat Role:")
        self.layout.addWidget(self.combat_role_label, 1, 0)
        self.combat_role_cbox = QComboBox()
        for item in self.config['Combat Roles']:
            self.combat_role_cbox.addItem(item)
        self.layout.addWidget(self.combat_role_cbox, 1, 1)

        # Create Combat Stance ComboBox.
        self.combat_stance_label = QLabel("Combat Stance:")
        self.layout.addWidget(self.combat_stance_label, 2, 0)
        self.combat_stance_cbox = QComboBox()
        for item in self.config['Combat Stances']:
            self.combat_stance_cbox.addItem(item)
        self.layout.addWidget(self.combat_stance_cbox, 2, 1)

        # Create Combat Role Variant ComboBox.
        self.combat_role_variant_label = QLabel("Role Variants:")
        self.layout.addWidget(self.combat_role_variant_label, 3, 0)
        if config['Combat Role Variations']:
            self.combat_role_variant_cbox = QComboBox()
            for item in self.config['Combat Role Variations']:
                self.combat_role_variant_cbox.addItem(item)
        else:
            self.combat_role_variant_cbox = QLabel("Not configured")
        self.layout.addWidget(self.combat_role_variant_cbox, 3, 1)

        # Create Combat Surges and Lulls ComboBox.
        self.combat_surge_lull_label = QLabel("Surges and/or Lulls:")
        self.layout.addWidget(self.combat_surge_lull_label, 4, 0)
        if config['Surges and Lulls']:
            self.combat_surge_lull_cbox = QComboBox()
            for item in self.config['Surges and Lulls']:
                self.combat_surge_lull_cbox.addItem(item)
        else:
            self.combat_surge_lull_cbox = QLabel("Not configured")
        self.layout.addWidget(self.combat_surge_lull_cbox, 4, 1)

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
    window = CombatModelerWindow(required_config_dfs, optional_config_dfs)
    window.show()
    sys.exit(app.exec())
