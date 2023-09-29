from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog, QComboBox, QLabel, QVBoxLayout, QWidget, QTableWidget, QMessageBox
from PyQt5 import QtCore, QtWidgets
import sys
import sqlite3
import pandas as pd
import os
import shutil

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
        
        self.total_item_label = QLabel(self.centralwidget)
        self.total_item_label.setGeometry(QtCore.QRect(160, 10, 220, 30))
        self.total_item_label.setObjectName("total_item_label")
        
        self.total_quantity_label = QLabel(self.centralwidget)
        self.total_quantity_label.setGeometry(QtCore.QRect(160, 50, 220, 30))
        self.total_quantity_label.setObjectName("total_quantity_label")
        
        self.total_weight_label = QLabel(self.centralwidget)
        self.total_weight_label.setGeometry(QtCore.QRect(160, 90, 220, 30))
        self.total_weight_label.setObjectName("total_weight_label")
        
        self.item_dropdown = QComboBox(self.centralwidget)
        self.item_dropdown.setGeometry(QtCore.QRect(400, 10, 150, 30))
        self.item_dropdown.setObjectName("item_dropdown")
        
        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 140, 760, 400))
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

        # Connect dropdown selection to function
        self.item_dropdown.currentIndexChanged.connect(self.update_item_stats)

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

        # Load items and update dropdown
        self.load_items()
        self.update_item_dropdown()

    def import_data(self):
        file_dialog = QFileDialog()
        file_paths, _ = file_dialog.getOpenFileNames(self, 'Select Files to Import', '', 'Excel Files (*.xlsx);;CSV Files (*.csv)')

        if file_paths:
            try:
                for file_path in file_paths:
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

                # After importing data, reload items and insert columns
                self.load_items()
                self.insert_columns(df.columns)

                # Display the imported data in the table
                self.display_data_in_table(df)

                QMessageBox.information(self, "Import Successful", "Data imported successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Import Error", f"Error while importing data: {str(e)}")

    def backup_data(self):
        backup_dir = QFileDialog.getExistingDirectory(self, 'Select Backup Directory', '')
        if backup_dir:
            backup_path = os.path.join(backup_dir, 'item_manager_backup.db')
            source_db_path = 'item_manager.db'

            try:
                shutil.copy(source_db_path, backup_path)
                QMessageBox.information(self, "Backup Successful", f"Database backed up to: {backup_path}")
            except Exception as e:
                QMessageBox.critical(self, "Backup Error", f"Error during backup: {str(e)}")

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

        # Calculate and display total item count, total quantity sum, and total weight sum
        total_item_count = len(rows)
        total_quantity_sum = sum(row[2] for row in rows)
        total_weight_sum = sum(row[3] for row in rows)
        self.total_item_label.setText(f"Total Items: {total_item_count}")
        self.total_quantity_label.setText(f"Total Quantity: {total_quantity_sum}")
        self.total_weight_label.setText(f"Total Weight: {total_weight_sum:.2f} kg")

    def insert_columns(self, columns):
        self.tableWidget.setColumnCount(len(columns))
        self.tableWidget.setHorizontalHeaderLabels(columns)

    def update_item_dropdown(self):
        # Clear existing items in the dropdown menu
        self.item_dropdown.clear()

        # Add a default item for selecting all items
        self.item_dropdown.addItem("All Items")

        # Get unique item names from the database
        self.cursor.execute("SELECT DISTINCT item FROM items")
        items = self.cursor.fetchall()

        # Add each item to the dropdown menu
        for item in items:
            self.item_dropdown.addItem(item[0])

    def display_data_in_table(self, df):
        # Display the full Excel sheet in the table widget
        self.tableWidget.setRowCount(len(df))
        for row_index, row_data in df.iterrows():
            for col_index, cell_value in enumerate(row_data):
                self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(cell_value)))

    def update_item_stats(self):
        selected_item = self.item_dropdown.currentText()

        if selected_item == "All Items":
            # Display total item count, total quantity sum, and total weight sum
            self.load_items()
        else:
            # Query the database for the selected item
            self.cursor.execute("SELECT * FROM items WHERE item=?", (selected_item,))
            rows = self.cursor.fetchall()
            self.tableWidget.setRowCount(0)  # Clear the table
            for row in rows:
                self.tableWidget.insertRow(self.tableWidget.rowCount())
                for col, value in enumerate(row[1:]):  # Skip the ID column
                    self.tableWidget.setItem(self.tableWidget.rowCount() - 1, col, QTableWidgetItem(str(value)))

            # Calculate and display total item count, total quantity sum, and total weight sum for the selected item
            total_item_count = len(rows)
            total_quantity_sum = sum(row[2] for row in rows)
            total_weight_sum = sum(row[3] for row in rows)
            self.total_item_label.setText(f"Total Items: {total_item_count}")
            self.total_quantity_label.setText(f"Total Quantity: {total_quantity_sum}")
            self.total_weight_label.setText(f"Total Weight: {total_weight_sum:.2f} kg")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ItemManagerApp()
    window.show()
    sys.exit(app.exec_())
