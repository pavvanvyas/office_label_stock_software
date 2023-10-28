import sys
import os
import sqlite3
import pandas as pd
import shutil
import pandas as pd
import csv
import psutil

from PyQt5.QtWidgets import QMessageBox

import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QAction, QComboBox, QLabel, QPushButton, QListWidget, QTableWidgetItem, QTableWidget, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont
# Add this import statement at the top of your script
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from ui import Ui_MainWindow

  
    
class ItemManagerApp(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()  # Initialize the main window
        self.ui = Ui_MainWindow()  # Create an instance of the Ui_MainWindow class
        self.ui.setupUi(self)  # Initialize the UI defined in Ui_MainWindow
        self.ui.set_styles()  # Apply styles
        self.ui.initialize_database()  # Initialize the database
        self.ui.import_button.clicked.connect(self.import_data)
       
     

    def initialize_database(self):
        # Check if the database file already exists
        if not os.path.isfile('item_manager.db'):
            # If the database file does not exist, create it with the desired column structure
            self.conn = sqlite3.connect('item_manager.db')
            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT * FROM items")
            self.conn.commit()
        else:
            # If the database file exists, connect to it
            self.conn = sqlite3.connect('item_manager.db')
            self.cursor = self.conn.cursor()

    
    def display_data_in_table(self, data):
    # Clear the existing table
      self.ui.tableWidget.setRowCount(0)

    # Set the number of columns in the QTableWidget based on the imported data
      self.ui.tableWidget.setColumnCount(len(data.columns))

      
       
      for col, header in enumerate(data.columns):
        self.ui.tableWidget.setHorizontalHeaderItem(col, QTableWidgetItem(str(header)))

      for row, row_data in data.iterrows():
        self.ui.tableWidget.insertRow(row)
        for col, value in enumerate(row_data):
            item = QTableWidgetItem(str(value))
            self.ui.tableWidget.setItem(row, col, item)

    def initUI(self):
        self.home_menu_action = QAction("Home", self)
     
        
        # Create a menu bar and add the action to it
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        file_menu.addAction(self.home_menu_action)
        
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Item Manager App")
        # Connect other signals and slots as needed
        # In your main application code or ItemManagerApp class
        self.home_menu_action = QAction("Home", self)
        self.home_menu_action.triggered.connect(self.toggle_home_screen)
        self.menuFile.addAction(self.home_menu_action)

        # Initialize the state variable

        # Add the "Home" menu action to your menu
        self.menuBar().addAction(self.ui.home_menu_action)

        
      
         # Apply styles here
        # Other initialization code goes here
        # Connect button click events to functions
          # Enable mouse tracking for the "Sell" button
       

        # Add the data_menu attribute to ItemManagerApp
            
        # Add the data_menu attribute to ItemManagerApp
       
        # After importing data, trigger recalculation of total weight
        
           
      
        # Add the data_menu attribute to ItemManagerApp
       
       
        self.import_button.clicked.connect(self.import_data)
        self.backup_button.clicked.connect(self.backup_data)
        self.delete_all_button.clicked.connect(self.delete_all_data)
        self.import_pendrive_button.clicked.connect(self.import_from_pendrive)
        self.delete_pendrive_button.clicked.connect(self.delete_from_pendrive)
        self.sell_button.clicked.connect(self.sell_item)
        self.show_sales_table_action.triggered.connect(self.toggle_sales_table)
        self.export_pendrive_action.triggered.connect(self.export_to_pendrive)

         # Access the data_menu attribute from the Ui_MainWindow class
        self.data_menu.addAction(self.export_pendrive_action)
         # Initialize the total weight label
        self.update_total_weight()
        # Connect to the SQLite database (or create it if it doesn't exist)
        self.conn = sqlite3.connect('item_manager.db')
        self.cursor = self.conn.cursor()

        # Create the table if it doesn't exist
        self.cursor.execute(('''CREATE TABLE IF NOT EXISTS items (
         SER_NO INTEGER PRIMARY KEY,
         GROSS REAL,
         LESS REAL,
         NET REAL,
         ITEM TEXT,
         CARAT REAL,
         HDR1 TEXT,
         HDR2 TEXT,
         HUID TEXT
          )'''))
        self.conn.commit()
    def toggle_home_screen(self):
        # Toggle the visibility of elements based on the state variable
        if self.is_home_screen_visible:
            # Hide all elements on the home screen
            self.tableWidget.hide()
            self.sales_table.hide()
            self.column_combobox.hide()
            self.export_pendrive_action.setVisible(False)  # Hide the export to pendrive action if needed
            # Hide other elements as needed
            self.is_home_screen_visible = False
        else:
            # Show all elements on the home screen
            self.tableWidget.show()
            self.sales_table.show()
            self.column_combobox.show()
            self.export_pendrive_action.setVisible(True)  # Show the export to pendrive action if needed
            # Show other elements as needed
            self.is_home_screen_visible = True

    def show_main_table(self):
        # Implement the logic to show or hide the main table
        if self.tableWidget.isHidden():
            self.tableWidget.show()
        else:
            self.tableWidget.hide()

    def setup_chart_actions(self):
        self.bar_chart_action = QAction("Bar Chart", self)
        self.bar_chart_action.triggered.connect(self.show_bar_chart)
        self.home_menu.addAction(self.bar_chart_action)
    
 

    def show_bar_chart(self):
     pass
  
    

    def scan_pendrive_for_files(self):
        pendrive_files = []

        for drive in psutil.disk_partitions():
            if 'removable' in drive.opts:
                drive_path = drive.device
                for root, _, files in os.walk(drive_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        file_name = os.path.basename(file_path)
                        pendrive_files.append((file_name, file_path))

        return pendrive_files
   
    

    
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
    
    def update_total_weight(self):
      pass
    
    def insert_item(self, gross, less, net, item, carat, hdr1, hdr2, huid):
      try:
        self.cursor.execute('''INSERT INTO items (GROSS, LESS, NET, ITEM, CARAT, HDR1, HDR2, HUID)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (gross, less, net, item, carat, hdr1, hdr2, huid))
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
        
   
    def export_table_to_csv(self, table_widget, file_path):
        # Export the data from a QTableWidget to a CSV file
        with open(file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            for row in range(table_widget.rowCount()):
                row_data = [table_widget.item(row, col).text() for col in range(table_widget.columnCount())]
                writer.writerow(row_data)

    def export_table_to_excel(self, table_widget, file_path):
        # Export the data from a QTableWidget to an Excel file using pandas
        import pandas as pd

        data = []
        headers = [table_widget.horizontalHeaderItem(col).text() for col in range(table_widget.columnCount())]
        for row in range(table_widget.rowCount()):
            row_data = [table_widget.item(row, col).text() for col in range(table_widget.columnCount())]
            data.append(row_data)

        df = pd.DataFrame(data, columns=headers)
        df.to_excel(file_path, index=False)

    def update_table(self):
    # Clear the existing table
        self.tableWidget.setRowCount(0)

    # Get the selected item from the dropdown menu
        selected_item = self.column_combobox.currentText()

    # Define the columns you want to select from the table
        columns = ["GROSS", "LESS", "NET", "ITEM", "CARAT", "HDR1", "HDR2", "HUID"]

    # Build the SQL query for selecting data based on the selected item
        if selected_item == "All Items":
          query = "SELECT " + ", ".join(columns) + " FROM items"
          self.cursor.execute(query)
        else:
          query = "SELECT " + ", ".join(columns) + " FROM items WHERE ITEM=?"
          self.cursor.execute(query, (selected_item,))

    # Fetch data from the database
        items = self.cursor.fetchall()

    # Populate the table widget with the fetched data
        for row_num, item in enumerate(items):
         self.tableWidget.insertRow(row_num)
        for col_num, value in enumerate(item):
            self.tableWidget.setItem(row_num, col_num, QTableWidgetItem(str(value)))


        
        items = self.cursor.fetchall()
        for row_num, item in enumerate(items):
            self.tableWidget.insertRow(row_num)
            for col_num, value in enumerate(item):
                self.tableWidget.setItem(row_num, col_num, QTableWidgetItem(str(value)))
        # Clear the existing table
        self.ui.tableWidget.setRowCount(0)

    # Fetch data from the database
        self.cursor.execute("SELECT * FROM items")
        items = self.cursor.fetchall()

    # Populate the table widget
        for row_num, item in enumerate(items):
         self.ui.tableWidget.insertRow(row_num)
        for col_num, value in enumerate(item):
            self.ui.tableWidget.setItem(row_num, col_num, QTableWidgetItem(str(value)))
    # After importing data, recalculate the total weight
    def recalculate_total_weight(self):
     total_weight = 0.0
     for row in range(self.tableWidget.rowCount()):
        weight_item = self.tableWidget.item(row, 2)  # Assuming weight is in the third column (index 2)
        if weight_item:
            total_weight += float(weight_item.text())

     # Update the total weight label
     self.total_weight_label.setText(f"Total Weight: {total_weight:.2f}")
    def delete_from_pendrive(self):
        # Get the selected file from the list widget
        selected_item = self.file_list_widget.currentItem()

        if selected_item:
            # Construct the full path to the selected file
            pendrive_path = "/media/pi"  # Update this path to match your pendrive's mount point
            file_path = os.path.join(pendrive_path, selected_item.text())

            try:
                # Delete the file from the pendrive
                os.remove(file_path)
                print(f"File '{selected_item.text()}' deleted from pendrive.")

            except Exception as e:
                print(f"Error while deleting from pendrive: {str(e)}")
    def sell_item(self):
    # Get the selected rows
        selected_rows = self.tableWidget.selectionModel().selectedRows()

        if not selected_rows:
         return  # No row selected

        for selected_row in selected_rows:
         item_name = self.tableWidget.item(selected_row.row(), 0).text()
        # If the item is not found in the sales table, insert it
         item_found = False
         sales_row_count = self.sales_table.rowCount()

        for row in range(sales_row_count):
            if self.sales_table.item(row, 0).text() == item_name:
                item_found = True
                break

        if not item_found:
            # Clone the selected row and insert it into the sales table
            sales_row = self.tableWidget.takeRow(selected_row.row())
            self.sales_table.insertRow(sales_row_count)
            self.sales_table.insertRow(sales_row)
            self.recalculate_total_weight()
    
    def import_data(self):
    # Open a file dialog to select the CSV file for import
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select File', '', 'CSV Files (*.csv)')

        if file_path:
         try:
            # Read the CSV file into a Pandas DataFrame with the ISO-8859-1 encoding
            data = pd.read_csv(file_path, encoding='iso-8859-1')  # Use ISO-8859-1 encoding

            # Ensure the imported data columns match the existing database columns
            existing_columns = [column[1] for column in self.cursor.execute('PRAGMA table_info(items)')]
            imported_columns = list(data.columns)

            if set(imported_columns) != set(existing_columns):
                QMessageBox.critical(self, "Error", "The columns in the CSV file do not match the existing database columns.")
                return

            # Append the data to the database
            data.to_sql('items', self.conn, if_exists='append', index=False)
            self.conn.commit()

            # Reload the data from the database and update the table
            self.update_table()
            self.recalculate_total_weight()

         except Exception as e:
            QMessageBox.critical(self, "Error", f"Error while importing data: {str(e)}")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ItemManagerApp()
    window.show()
    sys.exit(app.exec_())
