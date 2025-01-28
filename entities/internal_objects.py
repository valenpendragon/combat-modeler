import sys
import os
import time

import pandas as pd
import random
from functions import check_item

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
                 combat_tables_filepath, role_variant=None, individual_level=None):
        self.name = name
        self.combat_role = combat_role
        self.combat_stance = combat_stance
        self.difficulty = difficulty
        self.combat_workbook_filepath = combat_tables_filepath
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
        print(f"Character.__init__: {self}")
        print(f"Character.__init__: Initialization completed.")

    def clear_combat(self):
        """This method is required to clear the combat values when the
        Run Simulation button is pressed. It is included in the __init__()
        method rather than duplicate code."""
        print(f"Character.clear_combat: Clearing combat settings.")
        self.target = None
        self.action = None
        self.combat_action_table_name = None
        self.combat_action_table = None
        self.combat_targeting_table_name = None
        self.combat_targeting_table = None
        self.combat_status = 'Normal'
        print(f"Character.clear_combat: {self}")
        print(f"Character.clear_combat: clear_combat completed.")

    def update_status(self, name,  combat_role, combat_stance, difficulty,
                      role_variant=None, individual_level=None):
        """This method resets the values of the character, allowing even the
        name to be replaced. This is needed because a character dies and is
        replaced or because their role, stance, and/or role variant need to
        change during combat. Difficulty and individual level will change if
        character changes or the GM needs to tweak the combat."""
        print(f"Character.update_status: Update starting.")
        self.name = name
        self.combat_role = combat_role
        self.combat_stance = combat_stance
        self.difficulty = difficulty
        self.role_variant = role_variant
        self.level = individual_level
        self.clear_combat()
        self.create_table_names()
        print(f"Character.update_status: {self}")
        print(f"Character.update_status: update completed.")

    def create_table_names(self):
        """This method sets the Action and Targeting combat table names. It also
        calls the load_table() method to load and set these table attribute
        assignments."""
        print(f"Character.create_table_names: Beginning creation of table names and "
              f"loading tables.")
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
        print(f"Character.create_table_names: {self}")
        print(f"Character.create_table_names: pulling tables completed.")

    def validate_tables(self):
        """This method ensures that the combat action and targeting tables will
        be usable by this program. Other classes that use this will need to respond
        to a self.combat_action_table or self.combat_targeting_table being set to
        "invalid". It will also stop if the status of the table is already missing.
        This method returns no values. All changes are made in place."""
        print(f"Character.validate_tables: Beginning validation of tables to be used.")
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
            print(f"Character.validate_tables: cols: {cols}. action_cols: {action_cols}")
            print(f"Character.validate_tables: marking table invalid")
            self.combat_action_table = "invalid"
            errors += 1
        if cols != target_cols:
            print(f"Character.validate_tables: cols: {cols}. target_cols: {target_cols}")
            print(f"Character.validate_tables: marking table invalid")
            self.combat_targeting_table = "invalid"
            errors += 1
        if errors != 0:
            print(f"Character.validate_tables: {errors} have been generated. Action "
                  f"table, {action_table_name} or targeting table, {targeting_table_name} "
                  f"has an invalid format. Ending processing.")
            return
        print(f"Character.validate_tables: action table {action_table_name} and target "
              f"table {targeting_table_name} passed phase 1 validation.")

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
                if not check_item(item):
                    print(f"Character.validate_tables: item: {item} in table {action_table_name} "
                          f"failed validation")
                    self.combat_action_table = "invalid"
                    errors += 1
            for item in target_series:
                if not check_item(item):
                    print(f"Character.validate_tables: item: {item} in table "
                          f"{targeting_table_name} failed validation")
                    self.combat_targeting_table = "invalid"
                    errors += 1
            if errors != 0:
                print(f"Character.validate_tables: {errors} have been generated. Action "
                      f"table, {action_table_name} or targeting table, {targeting_table_name} "
                      f"has an invalid format. Ending processing.")
                return
            print(f"Character.validate_tables: action table {action_table_name} and target "
                  f"table {targeting_table_name} passed phase 2 validation.")

            # The final step is to make sure that the series in each table column
            # have sequential values with no gaps. self.check_series() is a static
            # method to perform that operation.
            if not self.check_series(action_series):
                bad_series = DIFFICULTY_VARIATIONS[n]
                print(f"Character.validate_tables: series {bad_series} in "
                      f"{action_table_name} is not sequential.")
                self.combat_action_table = "invalid"
                errors += 1
            if not self.check_series(target_series):
                bad_series = DIFFICULTY_VARIATIONS[n]
                print(f"Character.validate_tables: series {bad_series} in "
                      f"{targeting_table_name} is not sequential.")
                self.combat_targeting_table = "invalid"
                errors += 1
            if errors != 0:
                print(f"Character.validate_tables: {errors} have been generated. Action "
                      f"table, {action_table_name} or targeting table, {targeting_table_name} "
                      f"has an invalid format. Ending processing.")
                return
            print(f"Character.validate_tables: action table {action_table_name} and target "
                  f"table {targeting_table_name} passed phase 1 validation.")
            return

    @staticmethod
    def check_series(series: pd.DataFrame):
        """This static method checks a series to make sure that the actual integer
        values in the series are sequential and have no gaps. It returns True if everything
        checks out, False otherwise."""
        print(f"Character.check_series: Starting validation of series {series}.")
        filtered_series = series[lambda s: s != '-']
        print(f"Character.check_series: filtered_series: {filtered_series}")
        previous_value = 0
        errors = 0
        for item in filtered_series:
            l = item.split('-')
            low = int(l[0])
            if len(l) == 2:
                high = int(l[1])
            else:
                high = None
            print(f"Character.check_series: previous value: {previous_value} low: {low}, "
                  f"high: {high}, l: {l}, errors: {errors}")

            if low == 0 and high is None:
                low = 100
                print(f"Character.check_series: l: {l[0]} is zero and high is None. "
                      f"Setting low to {low}.")

            if previous_value != (low - 1):
                print(f"Character.check_series: previous value is not equal to low - 1.")
                errors += 1

            if high is not None:
                if high == 0:
                    high = 100
                    print(f"Character.check_series: low is {low}. h is {l[1]} which is zero. "
                          f"Setting high to {high}.")
                print(f"Character.check_series: checking value pair.")
                if low >= high:
                    print(f"Character.check_series: low:, {low}, is greater than or equal "
                          f"to high, {high}, Series failed sequential test.")
                    errors += 1
                previous_value = high
            else:
                previous_value = low

        print(f"Character.check_series: Series check completed with {errors} errors.")
        return errors == 0

    def load_table(self, table_name):
        """This method extracts the required table from self.combat_workbook_filepath and returns
        it. Note: Excel limits worksheet names to 31 characters.
        :param table_name: str, required
        :param combat_tables: filepath, optional, defaults to COMBAT_TABLES
        :return pd.DataFrame or str
        """
        combat_tables = self.combat_workbook_filepath
        print(f"Character.load_table: Beginning extraction of table {table_name} "
              f"from {combat_tables}.")
        xls = pd.ExcelFile(combat_tables)
        worksheet_name = table_name[:31]
        print(f"Character.load_table: table_name: {table_name}. "
              f"worksheet_name: {worksheet_name}.")
        try:
            table = pd.read_excel(xls, worksheet_name)
        except ValueError:
            print(f"Character.load_table: Table {worksheet_name} could not be found.")
            return "missing"
        print(f"Character.load_table: Table {table} found.")
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
        print(f"Character.roll_for_combat_action: Determining combat action.")
        difficulty = self.difficulty
        for item in self.combat_targeting_table.columns:
            if item.strip() == self.difficulty:
                difficulty = item
                print(f"Character.roll_for_combat_action: difficulty "
                      f"changed from {self.difficulty} to {difficulty}")
        try:
            table = self.combat_action_table[[difficulty, 'Outcome']]
        except KeyError:
            print(f"Character: roll_for_combat_action: KeyError discovered in table "
                  f"using {difficulty}. Could not complete task.")
            return
        except TypeError:
            print(f"Character: roll_for_combat_acton: TypeError discovered for "
                  f"{self.combat_targeting_table_name}. Cannot complete task.")
            return

        print(f"Character.roll_for_combat_action: action table: {table}")
        filtered_table = table[table[difficulty] != '-']
        print(f"Character.roll_for_combat_action: filtered action table: {filtered_table}")
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
        print(f"Character.roll_for_combat_action: {self}")
        print(f"Character.roll_for_combat_action: Combat action determined successfully.")

    def roll_for_combat_targeting(self):
        """This method finds the minimum and maximum values in the combat targeting table,
        generates a random number between the two values using a uniform distribution,
        and returns the text in the 'Outcome' column of the dataframe corresponding to
        that number. This result is assigned to Character.target."""
        # Grab the two columns we need from the table.
        print(f"Character.roll_for_combat_targeting: Determining target.")
        difficulty = self.difficulty
        for item in self.combat_targeting_table.columns:
            if item.strip() == self.difficulty:
                difficulty = item
                print(f"Character.roll_for_combat_targeting: difficulty "
                      f"changed from {self.difficulty} to {difficulty}")
        try:
            table = self.combat_targeting_table[[difficulty,'Outcome']]
        except KeyError:
            print(f"Character.roll_for_combat_targeting: KeyError discovered in "
                  f"table using {difficulty}. Could not complete task.")
            return
        print(f"Character.roll_for_combat_targeting: target_table: {table}")
        filtered_table = table[table[difficulty] != '-']
        print(f"Character.roll_for_combat_targeting: filtered target table: {filtered_table}")
        self.target = self.determine_result_from_table(filtered_table, difficulty)
        print(f"Character.roll_for_combat_targeting: {self}")
        print(f"Character.roll_for_combat_targeting: Target determination completed.")

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
        print(f"Character.determine_result_from_table: starting process.")
        print(f"Character.determine_result_from_table: filtered table: {filtered_table}")
        min_entry = filtered_table.iloc[0, 0]
        min_val = int(min_entry.split('-')[0])
        max_entry = filtered_table.iloc[-1, 0]
        max_val = self.return_int_from_table_item(max_entry)
        roll = random.randint(min_val, max_val)
        print(f"Character.determine_result_from_table: min: {min_val}. max: {max_val}. roll: {roll}")

        series = filtered_table[difficulty]
        idx = 0
        for item in series:
            list_values = item.split('-')
            print(f"Character.determine_result_from_table: idx: {idx}. item: {item}. "
                  f"list_values: {list_values}")
            comp_val = self.return_int_from_table_item(item)
            result = filtered_table['Outcome'].iloc[idx]
            print(f"Character.determine_result_from_table: comp_val: "
                  f"{comp_val}. roll: {roll} result: {result}")
            if roll > comp_val:
                idx += 1
                continue
            else:
                break
        print(f"Character.determine_result_from_table: Result, {result} determined.")
        return result

    @staticmethod
    def convert_table_string(s: str):
        """This static method takes a string of integers and converts it into a integer.
        If the integers are all zeros, it converts it into the correct power of ten."""
        print(f"Character.convert_table_string: Beginning string conversion.")
        len_s = len(s)
        if int(s) == 0:
            result = 10**len_s
        else:
            result = int(s)
        print(f"Character.convert_table_string: String converted to {result}.")
        return result

    def return_int_from_table_item(self, s: str, larger=True):
        print(f"Character.return_int_from_table_item: Pulling integer from item {s}.")
        list_s = s.split('-')
        len_list_s = len(list_s)
        if len_list_s == 1:
            result = self.convert_table_string(list_s[0])
        else:
            if larger:
                result = self.convert_table_string(list_s[1])
            else:
                result = self.convert_table_string(list_s[0])
        print(f"Character.return_int_from_table_item: Result is {result}.")
        return result


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
