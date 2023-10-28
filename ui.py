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
from PyQt5.QtGui import QFont
# Add this import statement at the top of your script
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtCore
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QAction, QComboBox, QLabel, QPushButton, QListWidget, QTableWidgetItem, QTableWidget, QWidget, QVBoxLayout, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from matplotlib.figure import Figure
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
     

# Create a menu bar
        self.menuBar = MainWindow.menuBar()

        
# Create the "Home" menu
        self.home_menu = self.menuBar.addMenu("Home")

        self.home_menu_action = QAction("Home", MainWindow)
        # Connect the action to the corresponding function
        self.home_menu_action.triggered.connect(self.toggle_home_screen)
           # Create a m enuFile attribute for your main window
        self.menuFile = MainWindow.menuBar().addMenu("File")
        self.export_pendrive_action = QtWidgets.QAction(MainWindow)
        self.home_menu_action.triggered.connect(self.on_home_triggered)
        # Assuming QMainWindow is the parent widget
        # Ensure that you have correctly defined self.export_pendrive_action in Ui_MainWindow
        self.menuFile.addAction(self.export_pendrive_action)
        # Add the "Home" menu action to your main menu (menuFile in this case)
        self.menuFile.addAction(self.home_menu_action)
         
        self.is_home_screen_visible = True 
      

        # Create a QAction for displaying the main table
        self.show_main_table_action = QAction("Show Main Table", MainWindow)
        self.home_menu.addAction(self.show_main_table_action)
        # Create the "Stock" menu
        self.stock_menu = MainWindow.menuBar().addMenu("Stock")

        # Create a QAction for displaying the main table in the Stock section
        self.show_main_table_action = QAction("Show Main Table", MainWindow)
        self.stock_menu.addAction(self.show_main_table_action)

        # Create the "Sales" menu
        self.sales_menu = MainWindow.menuBar().addMenu("Sales")

        
        # Add a Data menu to the menu bar
        self.data_menu = MainWindow.menuBar().addMenu("Data")
        # Create a QAction for displaying the sales table
        self.show_sales_table_action = QAction("Show Sales Table", MainWindow)
        self.sales_menu.addAction(self.show_sales_table_action)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # Create the export to pendrive action
        self.export_pendrive_action = QAction("Export to Pendrive",MainWindow)
        self.export_pendrive_action.triggered.connect(self.export_to_pendrive)
        self.menuFile.addAction(self.export_pendrive_action)
         # Add the export to pendriaction to the Data menu
        self.data_menu.addAction(self.export_pendrive_action)
        self.is_home_screen_visible = True
        self.layout = QVBoxLayout()

        self.tableWidget = QTableWidget()
        self.tableWidget.setObjectName("main_table")
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(["GROSS", "LESS", "NET", "ITEM", "CARAT", "HDR1", "HDR2", "HUID"])
        self.tableWidget.show()

        self.total_weight_label = QLabel()
        self.total_weight_label.setObjectName("total_weight_label")
        self.total_weight_label.setText("Total Weight: ")
       
        self.total_weight_label.setText("Total Weight: ")
        self.button_layout = QHBoxLayout()

        self.delete_all_button = QPushButton()
        self.delete_all_button.setObjectName("delete_all_button")
        self.delete_all_button.setText("Delete All Data")

   
        self.button_layout = QHBoxLayout()
        self.sell_button = QPushButton()
        self.sell_button.setObjectName("sell_button")
        self.sell_button.setText("Sell")
        self.sell_button.setEnabled(True)

        self.sales_table = QTableWidget()
        self.sales_table.setObjectName("sales_table")
        self.sales_table.setColumnCount(8)
        header_labels = ["GROSS", "LESS", "NET", "ITEM", "CARAT", "HDR1", "HDR2", "HUID"]
        self.sales_table.setHorizontalHeaderLabels(header_labels)

         # Connect the "Show Main Table" menu action to the toggle_main_table function
        self.show_main_table_action.triggered.connect(self.toggle_main_table)
        # Connect the "Show Sales Table" menu action to the toggle_sales_table function
        self.show_sales_table_action.triggered.connect(self.toggle_sales_table)


        self.show_sales_table_action.triggered.connect(self.toggle_sales_table)
        self.sales_table.show ()
         # If the item is not in the sales table, add it
        #self.sales_table.insertRow(sales_row_count)
        #self.sales_table.setItem(sales_row_count, 0, QTableWidgetItem(item_name))
       # self.sales_table.setItem(sales_row_count, 1, QTableWidgetItem("1"))  # You can modify this to sell multiple items at once

        # Update the total weight label and any other relevant calculations
        self.update_total_weight()
        self.column_combobox = QComboBox()
        self.column_combobox.setObjectName("column_combobox")

        self.import_button = QPushButton()
        self.import_button.setObjectName("import_button")
        self.import_button.setText("Import Data")

        self.backup_button = QPushButton()
        self.backup_button.setObjectName("backup_button")
        self.backup_button.setText("Backup Data")

        self.import_pendrive_button = QPushButton()
        self.import_pendrive_button.setObjectName("import_pendrive_button")
        self.import_pendrive_button.setText("Scan Pendrive")
        self.import_pendrive_button.clicked.connect(self.import_from_pendrive)

        self.file_list_widget = QListWidget()
        self.file_list_widget.setObjectName("file_list_widget")

        
        self.delete_pendrive_button = QPushButton()
        self.delete_pendrive_button.setObjectName("delete_pendrive_button")
        self.delete_pendrive_button.setText("Clean Pendrive")

        self.layout.addWidget(self.tableWidget)
        self.layout.addWidget(self.total_weight_label)
        self.layout.addLayout(self.button_layout)

        self.button_layout.addWidget(self.delete_all_button)
        self.button_layout.addWidget(self.sell_button)

        self.layout.addWidget(self.sales_table)
        self.layout.addWidget(self.column_combobox)
        self.layout.addWidget(self.import_button)
        self.layout.addWidget(self.backup_button)
        self.layout.addWidget(self.import_pendrive_button)
        self.layout.addWidget(self.file_list_widget)
      
        self.layout.addWidget(self.delete_pendrive_button)
    
        self.column_combobox.currentIndexChanged.connect(self.filter_and_display)



# Create sub-actions within the Data menu
        self.import_data_action = QAction("Import Data", MainWindow)
        self.export_data_action = QAction("Export Data", MainWindow)
        self.import_pendrive_action = QAction("Import from Pendrive", MainWindow)
        self.export_pendrive_action = QAction("Export to Pendrive", MainWindow)

  # Create the export to pendrive action
        self.export_pendrive_action = QAction("Export to Pendrive", MainWindow)
        self.export_pendrive_action.triggered.connect(self.export_to_pendrive)
        self.menuFile.addAction(self.export_pendrive_action)
         # Add the export to pendriaction to the Data menu
        self.data_menu.addAction(self.export_pendrive_action)
# Add the sub-actions to the Data menu
      # Add the sub-actions to the Data menu
        self.data_menu.addAction(self.import_data_action)
        self.data_menu.addAction(self.export_data_action)
        self.data_menu.addSeparator()
        self.data_menu.addAction(self.import_pendrive_action)
        self.data_menu.addAction(self.export_pendrive_action)
        
       # Connect these actions to your corresponding functions
        self.import_data_action.triggered.connect(self.import_data)
        self.export_data_action.triggered.connect(self.export_data)
        self.import_pendrive_action.triggered.connect(self.import_from_pendrive)
        self.export_pendrive_action.triggered.connect(self.export_to_pendrive)
    
     # Create a QAction for chart-related functionality
        self.chart_action = QAction("Show Chart", MainWindow)
        self.chart_action.triggered.connect(self.show_chart)
        self.menuFile.addAction(self.chart_action)


        self.centralwidget.setLayout(self.layout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Set styles
        self.set_styles()
    
    def set_styles(self):
     self.centralwidget.setStyleSheet("""
    /* Apply styles to the entire application */
   
    QMainWindow {
        background-color: #f0f0f0;
    }

    /* Apply styles to widgets */
    QWidget {
        background-color: #f0f0f0;
    }

    QTableWidget {
        background-color: white;
        border: 1px solid #ccc;
    }

    QPushButton {
        background-color: #007acc;
        color: white;
        border: 2px solid #007acc; /* Add a border */
        padding: 8px 16px; /* Adjust padding for a smaller button */
        border-radius: 4px; /* Smaller border radius */
        font-size: 14px; /* Smaller font size */
    }

    QPushButton:hover {
        background-color: #005d99;
        border: 2px solid #005d99; /* Change border color on hover */
    }

    QLabel {
        color: #333;
        font-size: 14px;
    }

    QComboBox {
        background-color: white;
        border: 1px solid #ccc;
        padding: 4px;
        border-radius: 5px;
    }
    
    /* Customize other widgets as needed */

    /* Apply specific styles to individual widgets if necessary */
    /* Example: */
    /* #myWidgetId {
        background-color: #ccc;
    } */
    """)
 

        # You can add more style definitions for other widgets as needed
   
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Item Manager"))
        # Translate other labels and buttons as needed
     # Add this method to your Ui_MainWindow class
    def update_data_menu_quantity(self, item_name, new_quantity):
      for action in self.data_menu.actions():
        if action.text().startswith(item_name):
            action.setText(f"{item_name} ({new_quantity} left)")
    def initialize_database(self):
        # Connect to the SQLite database (or create it if it doesn't exist)
         self.conn = sqlite3.connect('item_manager.db')
         self.cursor = self.conn.cursor()

    # Create the table if it doesn't exist with the desired column names
         self.cursor.execute('''CREATE TABLE IF NOT EXISTS items (
          SER_NO INTEGER PRIMARY KEY,
          GROSS REAL,
          LESS REAL,
          NET REAL,
          ITEM TEXT,
          CARAT REAL,
          HDR1 TEXT,
          HDR2 TEXT,
          HUID TEXT
           )''')
         self.conn.commit()
    def delete_all_data(self):
        
        reply = QtWidgets.QMessageBox.question(self, "Delete All Data", "Are you sure you want to delete all data?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            try:
                # Delete all data from the database
                self.cursor.execute("DELETE FROM items")
                self.conn.commit()

                # Clear the table and update the total weight label
                self.tableWidget.setRowCount(0)
                self.update_total_weight()

                # Clear the file list widget
                self.file_list_widget.clear()
            except Exception as e:
                print(f"Error while deleting all data: {str(e)}")
        # Implement the logic to delete all data here

    def toggle_home_screen(self):
        # Implement the logic to toggle the visibility of elements based on the state variable
        if self.is_home_screen_visible:
            # Hide elements on the home screen
            self.tableWidget.hide()
            self.sales_table.hide()
            self.column_combobox.hide()
            self.export_pendrive_action.setVisible(False)  # Hide the export to pendrive action if needed
            # Hide other elements as needed
            self.is_home_screen_visible = False
        else:
            # Show elements on the home screen
            self.tableWidget.show()
            self.sales_table.show()
            self.column_combobox.show()
            self.export_pendrive_action.setVisible(True)  # Show the export to pendrive action if needed
            # Show other elements as needed
            self.is_home_screen_visible = True
    
    def on_home_triggered(self):
    # Handle the action trigger here
        if self.is_home_screen_visible:
        # The home screen is currently visible, hide it
         self.tableWidget.hide()
         self.sales_table.hide()
         self.column_combobox.hide()
         self.export_pendrive_action.setVisible(False)  # Hide the export to pendrive action if needed
       # Hide other elements as needed
         self.is_home_screen_visible = False
        else:
         # The home screen is currently hidden, show it
         self.tableWidget.show()
         self.sales_table.show()
         self.column_combobox.show()
         self.export_pendrive_action.setVisible(True)  # Show the export to pendrive action if needed
        # Show other elements as needed
         self.is_home_screen_visible = True
    
    def export_to_pendrive(self):
        # Open a file dialog to select a directory on the pendrive
        selected_directory = QFileDialog.getExistingDirectory(self, 'Select Pendrive Directory', '/media')

        if selected_directory:
            # Now you have the selected directory path, you can export your data there
            export_path = selected_directory + '/exported_data.txt'  # Define your export file name

            try:
                # Here you can write your data export logic
                with open(export_path, 'w') as file:
                    file.write('This is exported data.\nYou can replace this with your actual data.')

                print(f'Data exported to: {export_path}')
            except Exception as e:
                print(f'Error exporting data: {str(e)}')
    
    def toggle_main_table(self):
        # Implement the logic to show or hide the main table
        self.tableWidget.hide()
        self.sales_table.show()
        # Populate the item_combobox with all items
        self.load_items()
        # Create a function to update the table with loaded data
        self.update_table()

        # Connect the dropdown menu's selection change event
        self.column_combobox.currentIndexChanged.connect(self.filter_and_display)

        # Connect the "Show Main Table" menu action to the toggle_main_table function
        self.show_main_table_action.triggered.connect(self.toggle_main_table)

        # Connect the "Show Sales Table" menu action to the toggle_sales_table function
        self.show_sales_table_action.triggered.connect(self.toggle_sales_table)

        # Initialize the total weight label
        self.update_total_weight()
    
    def toggle_sales_table(self):
        if self.sales_table.isHidden():
            self.sales_table.show()
            self.tableWidget.hide()
        else:
            self.sales_table.hide()
            self.tableWidget.show()
    def update_total_weight(self):
        # Calculate and display the total weight
        total_weight = 0.0
        for row in range(self.tableWidget.rowCount()):
            weight_item = self.tableWidget.item(row, 2)  # Assuming weight is in the third column (index 2)
            if weight_item:
                total_weight += float(weight_item.text())
        self.total_weight_label.setText(f"Total Weight: {total_weight:.2f}")
          
    def on_home_triggered(self):
        # Handle the action trigger here
        QMessageBox.information(self, "Home Action", "Home action triggered")

    
    
    def import_from_pendrive(self):
        pendrive_files = self.scan_pendrive_for_files()

        if not pendrive_files:
            QMessageBox.warning(self, "No Files Found", "No eligible files found in the pendrive for import.")
            return

        for file_name, file_path in pendrive_files:
            try:
                if file_path.lower().endswith('.csv'):
                    imported_data = pd.read_csv(file_path)
                elif file_path.lower().endswith('.xlsx'):
                    imported_data = pd.read_excel(file_path)
                else:
                    continue  # Skip unsupported file formats

                self.cursor.executemany("INSERT INTO items (item, quantity, weight) VALUES (?, ?, ?)",
                                        imported_data[['Item', 'Quantity', 'Weight']].values.tolist())
                self.conn.commit()

                # Optionally, you can delete the imported file from the pendrive
                os.remove(file_path)
                print(f"Data imported and file '{file_name}' deleted from pendrive.")
            except Exception as e:
                # Print the error message to help diagnose the issue
                print(f"Error while importing from {file_name}: {str(e)}")

            self.load_items()
            self.update_table()
            self.update_total_weight()
    
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

        self.recalculate_total_weight()
    
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
        # After importing data, reload items and update the table
        self.load_items()
        self.update_table()
        # After importing data, trigger recalculation of total weight
        self.recalculate_total_weight()
    
    def export_data(self):
        # Use QFileDialog to select the export location and format
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Data", "", "CSV Files (*.csv);;Excel Files (*.xlsx)", options=options)

        if file_path:
            try:
                if file_path.lower().endswith('.csv'):
                    # Export data to CSV
                    self.export_table_to_csv(self.tableWidget, file_path)
                    self.export_table_to_csv(self.sales_table, file_path)  # Export sales table as well
                elif file_path.lower().endswith('.xlsx'):
                    # Export data to Excel
                    self.export_table_to_excel(self.tableWidget, file_path)
                    self.export_table_to_excel(self.sales_table, file_path)  # Export sales table as well

                # Show a success message to the user
                QMessageBox.information(self, "Success", "Data exported successfully.")
            except Exception as e:
                # Handle any errors that may occur during the export process
                QMessageBox.critical(self, "Error", f"An error occurred during export: {str(e)}")
            
    def show_chart(self):
        # Create a Qt widget to embed the Matplotlib chart
        self.chart_widget = ChartWidget()
        self.chart_widget.setWindowTitle("Chart")
        self.chart_widget.show()

class ChartWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Create a Matplotlib Figure and Canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Plot your data (replace this with your actual data)
        self.plot_data()

    def plot_data(self):
        # Get a Matplotlib Axes to plot on
        ax = self.figure.add_subplot(111)

        # Add your data plotting logic here (e.g., ax.plot or ax.bar)
        # For example, let's create a simple line plot:
        x = [1, 2, 3, 4, 5]
        y = [10, 12, 5, 8, 15]
        ax.plot(x, y)

        # Set labels and title (customize as needed)
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")
        ax.set_title("Sample Chart")

        # Draw the chart
        self.canvas.draw()