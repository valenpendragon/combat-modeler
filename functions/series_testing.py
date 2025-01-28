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

