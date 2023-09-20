import sys
import os
import time

import pandas as pd
import random

COMBAT_TABLES_FILEPATH = './data/combat-tables.xlsx'
COMBAT_STATUSES = ['Normal', 'Minor Surge', 'Major Surge', 'Minor Lull', 'Major Lull']
DIFFICULTY_VARIATIONS = ['A', 'B', 'C', 'D']


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
        self.combat_status = 'Normal'
        self.create_table_names()
        # print(f"__init__: {self}")

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
        self.combat_status = 'Normal'
        # print(f"clear_combat: {self}")

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
        self.clear_combat()
        self.create_table_names()
        # print(f"update_status: {self}")

    def create_table_names(self):
        """This method sets the Action and Targeting combat table names. It also
        calls the load_table() method to load and set these table attribute
        assignments."""
        role = self.combat_role
        stance = self.combat_stance
        role_variant = self.role_variant
        if role_variant:
            action_table_name = f"{role} {role_variant} {stance} Action"
            targeting_table_name = f"{role} {role_variant} {stance} Targeting"
        else:
            action_table_name = f"{role} {stance} Action"
            targeting_table_name = f"{role} {stance} Targeting"
        self.combat_action_table_name = action_table_name
        self.combat_targeting_table_name = targeting_table_name
        self.combat_action_table = self.load_table(action_table_name)
        self.combat_targeting_table = self.load_table(targeting_table_name)
        self.validate_tables()
        # print(f"create_table_names: {self}")

    def validate_tables(self):
        """This method ensures that the combat action and targeting tables will
        be usable by this program. Other classes that use this will need to respond
        to a self.combat_action_table or self.combat_targeting_table being set to
        "invalid". It will also stop if the status of the table is already missing.
        """
        if isinstance(self.combat_action_table, str):
            return
        if isinstance(self.combat_targeting_table, str):
            return

        action_table = self.combat_action_table
        action_table_name = self.combat_action_table_name
        targeting_table = self.combat_targeting_table
        targeting_table_name = self.combat_targeting_table_name
        action_cols = [col.strip() for col in action_table.columns]
        target_cols = [col.strip() for col in targeting_table.columns]
        cols = DIFFICULTY_VARIATIONS.copy()
        cols.append('Outcome')
        errors = 0
        if cols != action_cols:
            print(f"validate_tables: cols: {cols}. action_cols: {action_cols}")
            print(f"validate_tables: marking table invalid")
            self.combat_action_table = "invalid"
            errors += 1
        if cols != target_cols:
            print(f"validate_tables: cols: {cols}. target_cols: {target_cols}")
            print(f"validate_tables: marking table invalid")
            self.combat_targeting_table = "invalid"
            errors += 1
        if errors != 0:
            return

        # The columns of the tables are correct or an approximate match.
        # Now, the contents of each columns need to checked. Columns A through
        # D (columns[0] to columns[3) must contain one of the following: a dash
        # "-" string for not applicable, a string or integer that can contain
        # leading zeros or be composed of zeros, or two integers connected by a
        # dash "-" character indicating a range of values. The left value must be
        # less than or equal to the right value. The fifth column is a string.
        for n in range(0, 4):
            action_series = action_table[action_table.columns[n]]
            target_series = targeting_table[targeting_table.columns[n]]
            for item in action_series:
                if not self.check_item(item):
                    print(f"validating_tables: item: {item} in table {action_table_name} failed validation")
                    self.combat_action_table = "invalid"
                    errors += 1
            for item in target_series:
                if not self.check_item(item):
                    print(f"validating_tables: item: {item} in table {targeting_table_name} failed validation")
                    self.combat_targeting_table = "invalid"
                    errors += 1
            if errors != 0:
                return

    @staticmethod
    def check_item(item: str) -> bool:
        """This static method checks a string to see if the format is correct for
        combat action or targeting tables. It returns True if so, False if not."""
        # print(f"check_item: item: {item}")
        if item == "-":
            return True
        l = item.split('-')
        # print(f"check_item: l: {l}.")
        if len(l) > 2:
            return False
        elif len(l) == 2:
            try:
                low = int(l[0])
                high = int(l[1])
                # print(f"check_item: low: {low}. high: {high}.")
            except ValueError:
                return False
            if low > high:
                return high == 0
            else:
                return True
        else:
            try:
                low = int(l[0])
                # print(f"check_item: low: {low}.")
            except ValueError:
                return False
        return True

    @staticmethod
    def load_table(table_name, combat_tables=COMBAT_TABLES_FILEPATH):
        """This method extracts the required table from COMBAT_TABLES and returns
        it. Note: Excel limits worksheet names to 31 characters.
        :param table_name: str, required
        :param combat_tables: filepath, optional, defaults to COMBAT_TABLES
        :return pd.DataFrame or str
        """
        xls = pd.ExcelFile(combat_tables)
        worksheet_name = table_name[:31]
        try:
            table = pd.read_excel(xls, worksheet_name)
        except ValueError:
            return "missing"
        # print(f"load_table: {table}")
        return table

    def __str__(self):
        output = f"Name: {self.name}. Role: {self.combat_role}.\n" \
                 f"Stance: {self.combat_stance}. Difficulty: {self.difficulty}.\n" \
                 f"Role Variant: {self.role_variant}. Level: {self.level}.\n" \
                 f"Status: {self.combat_status}. Target: {self.target}. Action: {self.action}.\n" \
                 f"Action Table Name: {self.combat_action_table_name}.\n" \
                 f"Targeting Table Name: {self.combat_targeting_table_name}.\n" \
                 f"Action Table: {self.combat_action_table}\n" \
                 f"Targeting Table: {self.combat_targeting_table}\n"
        return output

    def roll_for_combat_action(self):
        """This method finds the minimum and maximum values in the combat action table,
        generates a random number between the two values using a uniform distribution,
        and returns the text in the 'Outcome' column of the dataframe corresponding to
        that number. This result is assigned to Character.action."""
        # Grab the two columns we need from the table.
        difficulty = self.difficulty
        for item in self.combat_targeting_table.columns:
            if item.strip() == self.difficulty:
                difficulty = item
                print(f"difficulty changed from {self.difficulty} to {difficulty}")
        try:
            table = self.combat_action_table[[difficulty, 'Outcome']]
        except KeyError:
            print(f"roll_for_combat_action: KeyError discovered in table using {difficulty}")
            print(f"Could not complete task.")
            return
        except TypeError:
            print(f"roll_for_combat_acton: TypeError discovered for {self.combat_targeting_table_name}")
            print(f"Cannot complete task.")
            return

        # print(f"action table: {table}")
        filtered_table = table[table[difficulty] != '-']
        # print(f"filtered action table: {filtered_table}")
        self.action = self.determine_result_from_table(filtered_table, difficulty)

        # Generally, 'Normal' is not included in action outcomes. So, just in case,
        # the status_flag tracks changes that were included in the action outcome.
        # If none are found, it will default to 'Normal'.
        status_flag = False
        for status in COMBAT_STATUSES:
            if status.lower() in self.action.lower():
                self.combat_status = status
                status_flag = True
        if not status_flag:
            self.combat_status = 'Normal'
        print(f"roll_for_combat_action: {self}")

    def roll_for_combat_targeting(self):
        """This method finds the minimum and maximum values in the combat targeting table,
        generates a random number between the two values using a uniform distribution,
        and returns the text in the 'Outcome' column of the dataframe corresponding to
        that number. This result is assigned to Character.target."""
        # Grab the two columns we need from the table.
        difficulty = self.difficulty
        for item in self.combat_targeting_table.columns:
            if item.strip() == self.difficulty:
                difficulty = item
                # print(f"difficulty changed from {self.difficulty} to {difficulty}")
        try:
            table = self.combat_targeting_table[[difficulty,'Outcome']]
        except KeyError:
            print(f"KeyError discovered in table using {difficulty}")
            print(f"Could not complete task.")
            return
        # print(f"target table: {table}")
        filtered_table = table[table[difficulty] != '-']
        # print(f"filtered target table: {filtered_table}")
        self.target = self.determine_result_from_table(filtered_table, difficulty)
        # print(f"roll_for_combat_targeting: {self}")

    def determine_result_from_table(self, filtered_table, difficulty):
        """
        This method takes the difficulty (corrected version self.difficulty) and
        a filtered table taken from either self.combat_targeting_table or
        self.combat_action_table, determines the largest and smallest number for
        the roll possibilities in the table, generates a uniform distribution roll
        for that range of values, finds the text Outcome corresponding to roll, and
        returns that string.
        :param filtered_table: pd.DataFrame
        :param difficulty: str
        :return: str
        """
        print(f"determine_result_from_table: starting process")
        # print(f"filtered table: {filtered_table}")
        min_entry = filtered_table.iloc[0, 0]
        min_val = int(min_entry.split('-')[0])
        max_entry = filtered_table.iloc[-1, 0]
        max_val = self.return_int_from_table_item(max_entry)
        roll = random.randint(min_val, max_val)
        # print(f"min: {min_val}. max: {max_val}. roll: {roll}")

        series = filtered_table[difficulty]
        idx = 0
        for item in series:
            list_values = item.split('-')
            # print(f"idx: {idx}. item: {item}. list_values: {list_values}")
            comp_val = self.return_int_from_table_item(item)
            result = filtered_table['Outcome'].iloc[idx]
            # print(f"comp_val: {comp_val}. roll: {roll} result: {result}")
            if roll > comp_val:
                idx += 1
                continue
            else:
                break
        return result

    @staticmethod
    def convert_table_string(s: str):
        """This static method takes a string of integers and converts it into a integer.
        If the integers are all zeros, it convert it into the correct power of ten."""
        len_s = len(s)
        if int(s) == 0:
            return 10**len_s
        else:
            return int(s)

    def return_int_from_table_item(self, s: str, larger=True):
        list_s = s.split('-')
        len_list_s = len(list_s)
        if len_list_s == 1:
            return self.convert_table_string(list_s[0])
        else:
            if larger:
                return self.convert_table_string(list_s[1])
            else:
                return self.convert_table_string(list_s[0])


if __name__ == "__main__":
    COMBAT_TABLES_FILEPATH = '../data_orig/combat-tables.xlsx'
    print("main: First pass:")
    name = "Holy Knight"
    role = "Skirmisher"
    stance = "Relentless"
    difficulty = 'A'
    role_variant = "Solo"
    level = "Moderate"
    character = Character(name, role, stance, difficulty, role_variant, level)
    print(f"main: {character}")
    character.roll_for_combat_targeting()
    character.roll_for_combat_action()
    print(f"main: post-rolls: {character}")
    print(f"main: Second pass after reinforcements arrive and the Knight is injured.")
    character.update_status(name, combat_role='Brute', combat_stance='Bloodied',
                            difficulty='B', role_variant='Minion',
                            individual_level='Low')
    print(f"main: Second pass: {character}")
    character.roll_for_combat_targeting()
    character.roll_for_combat_action()
    print(f"main: post-rolls: {character}")
    print(f"main: Third pass: Knight has been healed up for most of their injuries.")
    character.update_status(name, combat_role='Skirmisher', combat_stance='Fresh',
                            difficulty='D', role_variant='Minion',
                            individual_level='Moderate')
    print(f"main: Third pass: {character}")
    character.roll_for_combat_targeting()
    character.roll_for_combat_action()
    print(f"main: post-rolls: {character}")
