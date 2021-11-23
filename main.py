import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class EspressoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        data = self.cur.execute("""SELECT * FROM coffee""").fetchall()
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(data[0]))
        self.titles = [elem[0] for elem in self.cur.description]
        for i, elem in enumerate(data):
            for j, val in enumerate(elem):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
        self.table.resizeColumnsToContents()
        self.ok_btn.clicked.connect(self.save_data)
        self.del_btn.clicked.connect(self.delete_rows)
        self.add_btn.clicked.connect(self.add_row)

    def get_data_from_table(self):
        data = []
        rows = self.table.rowCount()
        cols = self.table.columnCount()
        for row in range(rows):
            tmp = []
            for col in range(cols):
                tmp.append(self.table.item(row, col).text())
            data.append(tmp)
        return data

    def save_data(self):
        self.cur.execute("""DELETE FROM coffee""")
        data = self.get_data_from_table()
        for row in data:
            elems = [', '.join([f"\"{elem}\"" for elem in row[1:]])][0]
            elems = f"{row[0]}, " + elems
            print(elems)
            run = f"INSERT INTO coffee(id, variety, description, roast_level, type, price, " \
                  f"package_size), VALUES({elems})"
            print(run)
            self.cur.execute(run)
        self.con.commit()

    def add_row(self):
        self.table.setRowCount(self.table.rowCount() + 1)

    def delete_rows(self):
        rows = list(set([elem.row() for elem in self.table.selectedItems()]))
        for row in rows:
            self.table.removeRow(row)
        self.con.commit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    espresso_window = EspressoWindow()
    espresso_window.show()
    sys.exit(app.exec())
