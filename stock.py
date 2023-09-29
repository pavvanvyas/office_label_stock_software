import sys
import sqlite3
import pandas as pd
import shutil
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog, QPushButton
from PyQt5 import QtCore, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 300)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.import_button = QtWidgets.QPushButton(self.centralwidget)
        self.import_button.setGeometry(QtCore.QRect(20, 10, 120, 30))
        self.import_button.setObjectName("import_button")
        self.backup_button = QtWidgets.QPushButton(self.centralwidget)
        self.backup_button.setGeometry(QtCore.QRect(20, 50, 120, 30))
        self.backup_button.setObjectName("backup_button")
        self.usb_backup_button = QtWidgets.QPushButton(self.centralwidget)
        self.usb_backup_button.setGeometry(QtCore.QRect(20, 90, 120, 30))
        self.usb_backup_button.setObjectName("usb_backup_button")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(160, 10, 220, 280))
        self.tableWidget.setObjectName("tableWidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Item Manager"))
        self.import_button.setText(_translate("MainWindow", "Import Data"))
        self.backup_button.setText(_translate("MainWindow", "Backup Data"))
        self.usb_backup_button.setText(_translate("MainWindow", "USB Backup"))

class ItemManagerApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Connect button click events to functions
        self.import_button.clicked.connect(self.import_data)
        self.backup_button.clicked.connect(self.backup_data)
        self.usb_backup_button.clicked.connect(self.usb_backup_data)
        
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

    def import_data(self):
        file_dialog = QFileDialog()
        file_paths, _ = file_dialog.getOpenFileNames(self, 'Select Files to Import', '', 'Excel Files (*.xlsx);;CSV Files (*.csv)')

        if file_paths:
            for file_path in file_paths:
                try:
                    if file_path.endswith('.xlsx'):
                        # Import from Excel using pandas
                        df = pd.read_excel(file_path)
                    elif file_path.endswith('.csv'):
                        # Import from CSV using pandas
                        df = pd.read_csv(file_path)
                    else:
                        print(f"Unsupported file format: {file_path}")
                        continue

                    # Insert data into the database
                    for index, row in df.iterrows():
                        item = row['Item']
                        quantity = row['Quantity']
                        weight = row['Weight']
                        self.insert_item(item, quantity, weight)

                except Exception as e:
                    print(f"Error while importing from {file_path}: {str(e)}")

            # After importing data, reload items and insert columns
            self.load_items()
            self.insert_columns(df.columns)

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

    def usb_backup_data(self):
        usb_drive = QFileDialog.getExistingDirectory(self, 'Select USB Drive', '/media')
        if usb_drive:
            backup_path = os.path.join(usb_drive, 'item_manager_backup.db')
            source_db_path = 'item_manager.db'

            try:
                shutil.copy(source_db_path, backup_path)
                print(f"Database backed up to USB drive: {backup_path}")
            except Exception as e:
                print(f"Error during USB backup: {str(e)}")

    def insert_item(self, item, quantity, weight):
        try:
            self.cursor.execute("INSERT INTO items (item, quantity, weight) VALUES (?, ?, ?)", (item, quantity, weight))
            self.conn.commit()
        except Exception as e:
            print(f"Error while inserting item: {str(e)}")

    def load_items(self):
        self.tableWidget.setRowCount(0)
        self.cursor.execute("SELECT * FROM items")
        rows = self.cursor.fetchall()
        for row in rows:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            for col, value in enumerate(row[1:]):  # Skip the ID column
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, col, QTableWidgetItem(str(value)))

    def insert_columns(self, columns):
        self.tableWidget.setColumnCount(len(columns))
        self.tableWidget.setHorizontalHeaderLabels(columns)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ItemManagerApp()
    window.show()
    sys.exit(app.exec_())
