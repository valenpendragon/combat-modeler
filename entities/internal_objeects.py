import sys
import os
import pandas as pd
import random

COMBAT_TABLES = '../data/combat-tables.xlsx'


class Character:
    """
    This object stores values for each of up to ten characters that
    this project will handle. Combat Roles and Stances are taken from
    the options in the configuration tables and supplied by the
    CombatModeler window from user choices on dropdown boxes. The
    optional parameters are also provided from the same window.

    This class performs the operations to determine the action of the
    character and who, if anyone, they target.
    :param name: str, required (CombatModeler defaults it to the tab heading.
    :param combat_role: str, required
    :param combat_stance: str, required
    :param difficulty: str, required, chosen from DIFFICULTY_VARIATIONS
    :param role_variant: str, optional, defaults to None
    :param individual_level: str, optional, defaults to None,if used, it is chosen
        by the user from INDIVIDUAL_LEVEL
    """
    def __init__(self, name,  combat_role, combat_stance, difficulty,
                 role_variant=None, individual_level=None):
        self.name = name
        self.combat_role = combat_role
        self.combat_stance = combat_stance
        self.difficulty = difficulty
        self.role_variant = role_variant
        self.level = individual_level
        self.target = None
        self.action = None
        self.combat_action_table_name = None
        self.combat_action_table = None
        self.combat_targeting_table_name = None
        self.combat_targeting_table = None
        self.create_table_names()
        print(self)

    def clear_combat(self):
        """This method is required to clear the combat values when the
        Run Simulation button is pressed. It is included in the __init__()
        method rather than duplicate code."""
        self.target = None
        self.action = None
        self.combat_action_table_name = None
        self.combat_action_table = None
        self.combat_targeting_table_name = None
        self.combat_targeting_table = None
        print(self)

    def update_status(self, name,  combat_role, combat_stance, difficulty,
                      role_variant=None, individual_level=None):
        """This method resets the values of the character, allowing even the
        name to be replaced. This is needed because a character dies and is
        replaced or because their role, stance, and/or role variant need to
        change during combat. Difficulty and individual level will change if
        character changes or the GM needs to tweak the combat."""
        self.name = name
        self.combat_role = combat_role
        self.combat_stance = combat_stance
        self.difficulty = difficulty
        self.role_variant = role_variant
        self.level = individual_level
        self.create_table_names()
        print(self)

    def create_table_names(self):
        """This method sets the Action and Targeting combat table names. It also
        calls the load_table() method to load and set these table attribute
        assignments."""
        role = self.combat_role
        stance = self.combat_stance
        role_variant = self.role_variant
        action_table_name = f"{role} {role_variant} {stance} Action"
        targeting_table_name = f"{role} {role_variant} {stance} Targeting"
        self.combat_action_table_name = action_table_name
        self.combat_targeting_table_name = targeting_table_name
        self.combat_action_table = self.load_table(action_table_name)
        self.combat_targeting_table = self.load_table(targeting_table_name)
        print(self)

    def load_table(self, table_name, combat_tables=COMBAT_TABLES):
        """This method extracts the required table from COMBAT_TABLES and returns
        it. Note: Excel limits worksheet names to 31 characters.
        :param table_name: str, required
        :param combat_tables: filepath, optional, defaults to COMBAT_TABLES
        :return pd.DataFrame
        """
        xls = pd.ExcelFile(combat_tables)
        worksheet_name = table_name[:31]
        table = pd.read_excel(xls, worksheet_name)
        print(f"table: {table}")
        return table

    def __str__(self):
        output = f"Name: {self.name}. Role: {self.combat_role}.\n" \
                 f"Stance: {self.combat_stance}. Difficulty: {self.difficulty}.\n" \
                 f"Role Variant: {self.role_variant}. Level: {self.level}.\n" \
                 f"Target: {self.target}. Action: {self.action}.\n" \
                 f"Action Table Name: {self.combat_action_table_name}.\n" \
                 f"Targeting Table Name: {self.combat_targeting_table_name}.\n" \
                 f"Action Table: {self.combat_action_table}\n" \
                 f"Targeting Table: {self.combat_targeting_table}\n"
        return output


if __name__ == "__main__":
    name = "Holy Knight"
    role = "Skirmisher"
    stance = "Relentless"
    difficulty = 'A'
    role_variant = "Solo"
    level = "Moderate"
    character = Character(name, role, stance, difficulty, role_variant, level)
    print(character)
