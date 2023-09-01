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
        self.clear_tab_data_button = QPushButton("Clear Tab Data")
        self.clear_tab_data_button.clicked.connect(self.clear_tabs)
        self.toolbar.addWidget(self.clear_tab_data_button)
        self.close_window_button = QPushButton("Close Window")
        self.close_window_button.clicked.connect(self.close_simulator)
        self.toolbar.addWidget(self.close_window_button)

        mainLayout.addWidget(self.toolbar, 2, 0, 2, 0)

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
        ctr = 0
        for i in range(self.tab_widget1.count()):
            if self.tab_widget1.widget(i).status:
                # Generate an action and a target.
                self.tab_widget1.widget(i).character.roll_for_combat_action()
                self.tab_widget1.widget(i).character.roll_for_combat_targeting()

                # Pull out the data that is needed.
                name = self.tab_widget1.widget(i).character.name
                action = self.tab_widget1.widget(i).character.action
                target = self.tab_widget1.widget(i).character.target

                self.text_display.append(
                    f"<p>{name} targets {target} with {action}</p>")
                ctr += 1
            else:
                continue

        for i in range(self.tab_widget2.count()):
            if self.tab_widget2.widget(i).status:
                self.tab_widget2.widget(i).character.roll_for_combat_action()
                self.tab_widget2.widget(i).character.roll_for_combat_targeting()
                # Do an abbreviation check here later in development.
                name = self.tab_widget2.widget(i).character.name
                action = self.tab_widget2.widget(i).character.action
                target = self.tab_widget2.widget(i).character.target
                self.text_display.append(f"<p>{name} targets {target} with {action}</p>")
                ctr += 1
            else:
                continue

        if ctr == 0:
            self.text_display.append(f"<p><b>No tabs are active currently.</b></p>")

    def clear_tabs(self):
        """Reinitialize the window."""
        self.text_display.clear()
        self.tab_widget1.clear()
        self.tab_widget2.clear()
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
        self.tab_widget1.addTab(self.tab0, "One")
        self.tab_widget1.addTab(self.tab1, "Two")
        self.tab_widget1.addTab(self.tab2, "Three")
        self.tab_widget1.addTab(self.tab3, "Four")
        self.tab_widget1.addTab(self.tab4, "Five")
        self.tab_widget2.addTab(self.tab5, "Six")
        self.tab_widget2.addTab(self.tab6, "Seven")
        self.tab_widget2.addTab(self.tab7, "Eight")
        self.tab_widget2.addTab(self.tab8, "Nine")
        self.tab_widget2.addTab(self.tab9, "Ten")

    def save_tab_data(self):
        pass

    def load_tab_data(self):
        pass

    def close_simulator(self):
        self.close()


class CharacterTab(QWidget):
    def __init__(self, parent, config, name):
        super().__init__(parent)
        self.config = config

        # Create character assigned to this tab.
        self.name = name
        self.combat_role = config['Combat Roles'][0]
        self.combat_stance = config['Combat Stances'][0]
        self.difficulty = config['Relative Difficulty'][0]
        if config['Combat Role Variations'] is not None:
            self.role_variant = config['Combat Role Variations'][0]
        else:
            self.role_variant = None
        if config['Surges and Lulls'] is not None:
            self.level = INDIVIDUAL_LEVEL[0]
        else:
            self.level = None
        self.character = Character(name = self.name,
                                   combat_role=self.combat_role,
                                   combat_stance=self.combat_stance,
                                   difficulty=self.difficulty,
                                   role_variant=self.role_variant,
                                   individual_level=self.level)

        # Set up tab layout and widget content.
        self.layout = QGridLayout()
        self.tab_name_label = QLabel("Set Name:")
        self.layout.addWidget(self.tab_name_label, 0, 0)
        self.name_input = QLineEdit(self)
        self.name_input.setText(self.name)
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

        # Create Combat Difficulty ComboBox.
        self.difficulty_label = QLabel("Encounter Difficulty:")
        self.layout.addWidget(self.difficulty_label, 3, 0)
        self.difficulty_cbox = QComboBox()
        for item in self.config['Relative Difficulty']:
            self.difficulty_cbox.addItem(item)
        self.layout.addWidget(self.difficulty_cbox, 3, 1)

        # Create Combat Role Variant ComboBox.
        self.combat_role_variant_label = QLabel("Role Variants:")
        self.layout.addWidget(self.combat_role_variant_label, 4, 0)
        if config['Combat Role Variations']:
            self.combat_role_variant_cbox = QComboBox()
            for item in self.config['Combat Role Variations']:
                self.combat_role_variant_cbox.addItem(item)
        else:
            self.combat_role_variant_cbox = QLabel("Not configured")
        self.layout.addWidget(self.combat_role_variant_cbox, 4, 1)

        # Create Combat Surges and Lulls ComboBox.
        self.combat_surge_lull_label = QLabel("Surges and/or Lulls:")
        self.layout.addWidget(self.combat_surge_lull_label, 5, 0)
        if config['Surges and Lulls']:
            self.combat_surge_lull_cbox = QComboBox()
            for item in self.config['Surges and Lulls']:
                self.combat_surge_lull_cbox.addItem(item)
        else:
            self.combat_surge_lull_cbox = QLabel("Not configured")
        self.layout.addWidget(self.combat_surge_lull_cbox, 5, 1)

        # Create Toggle Active button and QLabel to show status.
        # There is also an attribute to store this status.
        self.toggle_active_button = QPushButton("Toggle Active")
        self.status = False
        self.status_label = QLabel("Inactive")
        self.toggle_active_button.clicked.connect(self.toggle_status)
        self.layout.addWidget(self.toggle_active_button, 6, 0)
        self.layout.addWidget(self.status_label, 6, 1)

        # Create tab button to update character data for the tab.
        self.update_button = QPushButton("Update Character")
        self.update_button.clicked.connect(self.update_character)
        self.layout.addWidget(self.update_button, 7, 0)

        self.setLayout(self.layout)

    def update_character(self):
        self.name = self.name_input.text()
        self.combat_role = self.combat_role_cbox.currentText()
        self.combat_stance = self.combat_stance_cbox.currentText()
        self.difficulty = self.difficulty_cbox.currentText()
        # __init__() set self.roll_variant to None if config has it as None.
        if self.config['Combat Role Variations'] is not None:
            self.role_variant = self.combat_role_variant_cbox.currentText()
        # __init__() set self.level to None if config has it as None.
        if self.config['Surges and Lulls'] is not None:
            self.level = self.combat_surge_lull_cbox.currentText()
        self.character.update_status(name=self.name,
                                     combat_role=self.combat_role,
                                     combat_stance=self.combat_stance,
                                     difficulty=self.difficulty,
                                     role_variant=self.role_variant,
                                     individual_level=self.level)

    def toggle_status(self):
        """This status determines whether or not the character will be used
        when the Run Simulation button is clicked in the CharacterModeler
        window."""
        if self.status:
            self.status = False
            self.status_label.setText("Inactive")
        else:
            self.status = True
            self.status_label.setText("<b>Active</b>")


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
