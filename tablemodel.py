#!/usr/bin/python

# use PyQT's QTableView and QAbstractTableModel
# to present tabular data (with column sort option)
# tested with Python 3.1 and PyQT 4.5
# Henri

import operator
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MyWindow(QWidget):
    def __init__(self, element_list, header, *args):
        QWidget.__init__(self, *args)
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(300, 200, 460, 300)
        self.setWindowTitle("Sorting PyQT's QTableView")

        self.header = header
        self.mydata = element_list
        # create table
        table = self.createTable()

        # use vbox layout
        layout = QVBoxLayout()
        layout.addWidget(table)
        self.setLayout(layout)

    def createTable(self):
        # create table view
        tview = QTableView()
        # set table model
        tmodel = MyTableModel(self, self.mydata, self.header)
        tview.setModel(tmodel)
        # set minimum size of table
        tview.setMinimumSize(450, 300)
        # hide grid
        tview.setShowGrid(False)
        # set font
        font = QFont("Courier New", 8)
        tview.setFont(font)
        # hide vertical header
        vh = tview.verticalHeader()
        vh.setVisible(False)
        # set horizontal header properties
        hh = tview.horizontalHeader()
        hh.setStretchLastSection(True)
        # set column width to fit contents
        tview.resizeColumnsToContents()
        # set all row heights
        nrows = len(self.mydata)
        for row in range(nrows):
            tview.setRowHeight(row, 18)
        # enable sorting
        tview.setSortingEnabled(True)
        return tview

class MyTableModel(QAbstractTableModel):
    def __init__(self, parent, mydata, header, *args):
        """
        mydata is list of tuples
        header is list of strings
        tuple length has to match header length
        """
        QAbstractTableModel.__init__(self, parent, *args)
        self.mydata = mydata
        self.header = header

    def rowCount(self, parent):
        return len(self.mydata)

    def columnCount(self, parent):
        return len(self.mydata[0])

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.mydata[index.row()][index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.header[col])
        return QVariant()

    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.mydata = sorted(self.mydata,
            key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.mydata.reverse()
        self.emit(SIGNAL("layoutChanged()"))


# the test data is from one of vegaseat's codes
# so if there is a mistake don't blame Henri ...
header = [' Symbol ', ' Name ', ' Atomic Weight ', ' Melt (K) ', ' Boil (K) ']
# use numbers for numeric data to sort properly
element_list = [
('H', 'Hydrogen', 1.00794, 13.81, 20.28),
('He', 'Helium', 4.0026, 0.95, 4.216),
('Li', 'Lithium', 6.941, 453.7, 1615),
('Be', 'Beryllium', 9.0122, 1560, 3243),
('B', 'Boron', 10.811, 2365, 4275),
('C', 'Carbon', 12.011, 3825, 5100),
('N', 'Nitrogen', 14.0067, 63.15, 77.344),
('O', 'Oxygen', 15.9994, 54.8, 90.188),
('F', 'Fluorine', 18.9984, 53.65, 85.0),
('Ne', 'Neon', 20.1797, 24.55, 27.1),
('Na', 'Sodium', 22.98977, 371.0, 1156),
('Mg', 'Magnesium', 24.305, 922, 1380),
('Al', 'Aluminum', 26.9815, 933.5, 2740),
('Si', 'Silicon', 28.0855, 1683, 2630),
('P', 'Phosphorus', 30.9737, 317.3, 553),
('S', 'Sulfur', 32.066, 392.2, 717.62),
('Cl', 'Chlorine', 35.4527, 172.17, 239.18),
('Ar', 'Argon', 39.948, 83.95, 87.45),
('K', 'Potassium', 39.0983, 336.8, 1033),
('Ca', 'Calcium', 40.078, 1112, 1757),
('Sc', 'Scandium', 44.9559, 1814, 3109),
('Ti', 'Titanium', 47.88, 1935, 3560),
('V', 'Vanadium', 50.9415, 2136, 3650),
('Cr', 'Chromium', 51.996, 2130, 2945),
('Mn', 'Manganese', 54.938, 1518, 2235),
('Fe', 'Iron', 55.847, 1808, 3023),
('Co', 'Cobalt', 58.9332, 1768, 3143),
('Ni', 'Nickel', 58.6934, 1726, 3005),
('Cu', 'Copper', 63.546, 1356.6, 2840),
('Zn', 'Zinc', 65.39, 682.73, 1180),
('Ga', 'Gallium', 69.723, 302.92, 2478),
('Ge', 'Germanium', 72.61, 1211.5, 3107),
('As', 'Arsenic', 74.9216, 876.4, 876.3),
('Se', 'Selenium', 78.96, 494, 958),
('Br', 'Bromine', 79.904, 265.95, 331.85),
('Kr', 'Krypton', 83.8, 116, 120.85),
('Rb', 'Rubidium', 85.4678, 312.63, 961),
('Sr', 'Strontium', 87.62, 1042, 1655),
('Y', 'Yttrium', 88.9059, 1795, 3611),
('Zr', 'Zirconium', 91.224, 2128, 4683),
('Nb', 'Niobium', 92.9064, 2743, 5015),
('Mo', 'Molybdenum', 95.94, 2896, 4912),
('Tc', 'Technetium', 98, 2477, 4538),
('Ru', 'Ruthenium', 101.07, 2610, 4425),
('Rh', 'Rhodium', 102.9055, 2236, 3970),
('Pd', 'Palladium', 106.42, 1825, 3240),
('Ag', 'Silver', 107.868, 1235.08, 2436),
('Cd', 'Cadmium', 112.41, 594.26, 1040),
('In', 'Indium', 114.82, 429.78, 2350),
('Sn', 'Tin', 118.71, 505.12, 2876),
('Sb', 'Antimony', 121.757, 903.91, 1860),
('Te', 'Tellurium', 127.6, 722.72, 1261),
('I', 'Iodine', 126.9045, 386.7, 457.5),
('Xe', 'Xenon', 131.29, 161.39, 165.1),
('Cs', 'Cesium', 132.9054, 301.54, 944),
('Ba', 'Barium', 137.33, 1002, 2079),
('La', 'Lanthanum', 138.9055, 1191, 3737),
('Ce', 'Cerium', 140.12, 1071, 3715),
('Pr', 'Praseodymium', 140.9077, 1204, 3785),
('Nd', 'Neodymium', 144.24, 1294, 3347),
('Pm', 'Promethium', 145, 1315, 3273),
('Sm', 'Samarium', 150.36, 1347, 2067),
('Eu', 'Europium', 151.965, 1095, 1800),
('Gd', 'Gadolinium', 157.25, 1585, 3545),
('Tb', 'Terbium', 158.9253, 1629, 3500),
('Dy', 'Dysprosium', 162.5, 1685, 2840),
('Ho', 'Holmium', 164.9303, 1747, 2968),
('Er', 'Erbium', 167.26, 1802, 3140),
('Tm', 'Thulium', 168.9342, 1818, 2223),
('Yb', 'Ytterbium', 173.04, 1092, 1469),
('Lu', 'Lutetium', 174.967, 1936, 3668),
('Hf', 'Hafnium', 178.49, 2504, 4875),
('Ta', 'Tantalum', 180.9479, 3293, 5730),
('W', 'Tungsten', 183.85, 3695, 5825),
('Re', 'Rhenium', 186.207, 3455, 5870),
('Os', 'Osmium', 190.2, 3300, 5300),
('Ir', 'Iridium', 192.22, 2720, 4700),
('Pt', 'Platinum', 195.08, 2042.1, 4100),
('Au', 'Gold', 196.9665, 1337.58, 3130),
('Hg', 'Mercury', 200.59, 234.31, 629.88),
('Tl', 'Thallium', 204.383, 577, 1746),
('Pb', 'Lead', 207.2, 600.65, 2023),
('Bi', 'Bismuth', 208.9804, 544.59, 1837),
('Po', 'Polonium', 209, 527, 1235.15),
('At', 'Astatine', 210, 575, 610),
('Rn', 'Radon', 222, 202, 211.4),
('Fr', 'Francium', 223, 300, 950),
('Ra', 'Radium', 226.0254, 973, 1413),
('Ac', 'Actinium', 227, 1324, 3470),
('Th', 'Thorium', 232.0381, 2028, 5060),
('Pa', 'Proctactinium', 231.0359, 1845, 4300),
('U', 'Uranium', 238.029, 1408, 4407),
('Np', 'Neptunium', 237.0482, 912, 4175),
('Pu', 'Plutonium', 244, 913, 3505),
('Am', 'Americium', 243, 1449, 2880),
]

app = QApplication(sys.argv)
win = MyWindow(element_list, header)
win.show()
sys.exit(app.exec_())
