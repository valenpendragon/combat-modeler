import numpy as np
import pandas as pd


def check_item(item: str) -> bool:
    """This static method checks a string to see if the format is correct for
    combat action or targeting tables. It returns True if so, False if not."""
    # print(f"check_item: item: {item}")
    print(f"Character.check_item: Starting validation of item, {item}.")
    if item == "-":
        return True
    l = item.split('-')
    print(f"Character.check_item: l: {l}.")
    if len(l) > 2:
        return False
    elif len(l) == 2:
        try:
            low = int(l[0])
            high = int(l[1])
            print(f"Character.check_item: low: {low}. high: {high}.")
        except ValueError:
            return False
        if low > high:
            return high == 0
        else:
            return True
    else:
        try:
            low = int(l[0])
            print(f"Character.check_item: low: {low}.")
        except ValueError:
            return False
    return True


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

