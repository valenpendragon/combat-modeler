import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
import pandas as pd


class ConfigTableModel(QAbstractTableModel):
    pass


class CombatActionTableModel(QAbstractTableModel):
    pass


class CombatTargetTableModel(QAbstractTableModel):
    pass
