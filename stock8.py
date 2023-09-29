import sys
import os
import sqlite3
import pandas as pd
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QComboBox, QTableWidgetItem
from PyQt5 import QtCore, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.import_button = QtWidgets.QPushButton(self.centralwidget)
        self.import_button.setGeometry(QtCore.QRect(20, 10, 120, 30))
        self.import_button.setObjectName("import_button")
        self.backup_button = QtWidgets.QPushButton(self.centralwidget)
        self.backup_button.setGeometry(QtCore.QRect(20, 50, 120, 30))
        self.backup_button.setObjectName("backup_button")
        self.column_combobox = QComboBox(self.centralwidget)
        self.column_combobox.setGeometry(QtCore.QRect(160, 10, 150, 30))
        self.column_combobox.setObjectName("column_combobox")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(160, 50, 620, 500))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Item", "Quantity", "Weight"])
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Item Manager"))
        self.import_button.setText(_translate("MainWindow", "Import Data"))
        self.backup_button.setText(_translate("MainWindow", "Backup Data"))

class ItemManagerApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Connect button click events to functions
        self.import_button.clicked.connect(self.import_data)
        self.backup_button.clicked.connect(self.backup_data)

        # Connect to the SQLite database (or create it if it doesn't exist)
        self.conn = sqlite3.connect('item_manager.db')
        self.cursor = self.conn.cursor()

        # Create the table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY,
            item TEXT,
            quantity INTEGER,
            weight REAL
        )''')
        self.conn.commit()

        # Populate the item_combobox with all items
        self.load_items()

        # Connect the dropdown menu's selection change event
        self.column_combobox.currentIndexChanged.connect(self.filter_and_display)

        # Initialize the table with all items
        self.update_table()

    def import_data(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select a File to Import', '', 'Excel Files (*.xlsx);;CSV Files (*.csv)')

        if file_path:
            try:
                if file_path.endswith('.xlsx'):
                    # Import from Excel using pandas
                    df = pd.read_excel(file_path)
                elif file_path.endswith('.csv'):
                    # Import from CSV using pandas
                    df = pd.read_csv(file_path)
                else:
                    print(f"Unsupported file format: {file_path}")
                    return

                # Prompt the user to select a column for the drop-down menu
                columns = df.columns.tolist()
                column, ok = QtWidgets.QInputDialog.getItem(self, "Select Column", "Select a column for the drop-down menu:", columns, 0, False)

                if ok:
                    # Insert data into the database
                    for index, row in df.iterrows():
                        item = row[column]
                        quantity = row['Quantity']
                        weight = row['Weight']
                        self.insert_item(item, quantity, weight)

                    # After importing data, reload items
                    self.load_items()
                    self.update_table()

            except Exception as e:
                print(f"Error while importing from {file_path}: {str(e)}")

    def backup_data(self):
        backup_dir = QFileDialog.getExistingDirectory(self, 'Select Backup Directory', '')
        if backup_dir:
            backup_path = os.path.join(backup_dir, 'item_manager_backup.db')
            source_db_path = 'item_manager.db'

            try:
                shutil.copy(source_db_path, backup_path)
                print(f"Database backed up to: {backup_path}")
            except Exception as e:
                print(f"Error during backup: {str(e)}")

    def insert_item(self, item, quantity, weight):
        try:
            self.cursor.execute("INSERT INTO items (item, quantity, weight) VALUES (?, ?, ?)", (item, quantity, weight))
            self.conn.commit()
        except Exception as e:
            print(f"Error while inserting item: {str(e)}")

    def load_items(self):
        self.column_combobox.clear()
        self.cursor.execute("SELECT DISTINCT item FROM items")
        items = self.cursor.fetchall()
        all_items = [item[0] for item in items]
        # Add an option for displaying all items
        self.column_combobox.addItem("All Items")
        # Populate the dropdown menu with all items
        self.column_combobox.addItems(all_items)

    def filter_and_display(self):
        # Get the selected item from the dropdown menu
        selected_item = self.column_combobox.currentText()

        # Clear the existing table
        self.tableWidget.setRowCount(0)

        # Fetch data from the database based on the selected item
        if selected_item == "All Items":
            # Fetch all items if "All Items" is selected
            self.cursor.execute("SELECT item, quantity, weight FROM items")
        else:
            # Fetch data based on the selected item
            self.cursor.execute("SELECT item, quantity, weight FROM items WHERE item=?", (selected_item,))

        items = self.cursor.fetchall()

        # Repopulate the table with filtered data
        for row_num, item in enumerate(items):
            self.tableWidget.insertRow(row_num)
            for col_num, value in enumerate(item):
                self.tableWidget.setItem(row_num, col_num, QTableWidgetItem(str(value)))
    def update_table(self):
        # Clear the existing table
        self.tableWidget.setRowCount(0)
           # Get the selected item from the dropdown menu
        selected_item = self.column_combobox.currentText()

       # Fetch data from the database based on the selected item
        if selected_item == "All Items":
       # Fetch all items if "All Items" is selected
         self.cursor.execute("SELECT item, quantity, weight FROM items")
        else:
         self.cursor.execute("SELECT item, quantity, weight FROM items WHERE item=?", (selected_item,))

        
        items = self.cursor.fetchall()
        for row_num, item in enumerate(items):
            self.tableWidget.insertRow(row_num)
            for col_num, value in enumerate(item):
                self.tableWidget.setItem(row_num, col_num, QTableWidgetItem(str(value)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ItemManagerApp()
    window.show()
    sys.exit(app.exec_())
