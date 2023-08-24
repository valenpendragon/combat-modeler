import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
import pandas as pd


class PandasModel(QAbstractTableModel):
    """Interface between Pandas DataFrame and Qt."""
    def __init__(self, dataframe: pd.DataFrame, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._dataframe = dataframe

    def rowCount(self, parent=QModelIndex()):
        """Override QAbstractTableModel method to return row count
        of a pandas dataframe."""
        if parent == QModelIndex():
            return self._dataframe.shape[0]
        return 0

    def columnCount(self, parent=QModelIndex()):
        """Override QAbstractTableModel method to return column count
        of a pandas dataframe."""
        if parent == QModelIndex():
            return self._dataframe.shape[1]
        return 0

    def data(self, index: QModelIndex, role=Qt.ItemDataRole):
        """Override QAbstractTableModel method to return str representation
        of the cell contents of a  pandas dataframe."""
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            return str(self._dataframe.iloc[index.row(), index.column()])

        return None

    def headerData(self, section: int,
                   orientation: Qt.Orientation,
                   role: Qt.ItemDataRole):
        """Override QAbstractTableModel method to return index as vertical
        header data and columns as horizontal header data."""
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._dataframe.columns[section])
            if orientation == Qt.Vertical:
                return str(self._dataframe.index[section])
        return None


class ConfigTableModel(PandasModel):
    pass


class CombatActionTableModel(PandasModel):
    pass


class CombatTargetTableModel(PandasModel):
    pass
