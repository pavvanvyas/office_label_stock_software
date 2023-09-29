import sys
import os
import sqlite3
import pandas as pd
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog,QAction,QVBoxLayout,QTableWidget,QWidget,QComboBox,QLabel,QPushButton,QListWidget
from PyQt5 import QtCore, QtWidgets
# Add this import statement at the top of your script
from PyQt5.QtWidgets import QTableWidgetItem
# Add these imports at the top of your script
from PyQt5.QtGui import QFont
# Your existing imports and code here...


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
         # Add a QLabel for displaying the total weight
        self.total_weight_label = QLabel(self.centralwidget)
        self.total_weight_label.setGeometry(QtCore.QRect(160, 560, 300, 30))
        self.total_weight_label.setObjectName("total_weight_label")
        self.total_weight_label.setText("Total Weight: ")
        
         # Add a QPushButton for deleting all data
        self.delete_all_button = QPushButton(self.centralwidget)
        self.delete_all_button.setGeometry(QtCore.QRect(350, 10, 120, 30))
        self.delete_all_button.setObjectName("delete_all_button")
        self.delete_all_button.setText("Delete All Data")
        
         # Add a QPushButton for importing data from pendrive
        self.import_pendrive_button = QPushButton(self.centralwidget)
        # Connect the "Import from Pendrive" button click event to the import_from_pendrive function
        self.import_pendrive_button.clicked.connect(self.import_from_pendrive)

        self.import_pendrive_button.setGeometry(QtCore.QRect(20, 90, 120, 30))
        self.import_pendrive_button.setObjectName("import_pendrive_button")
        self.import_pendrive_button.setText("scan pendrive")
        

        # Add a QListWidget to display file names from pendrive
        self.file_list_widget = QListWidget(self.centralwidget)
        self.file_list_widget.setGeometry(QtCore.QRect(20, 120, 120, 30))
        self.file_list_widget.setObjectName("file_list_widget")

        # Add a QPushButton to confirm import from pendrive
        self.confirm_import_button = QPushButton(self.centralwidget)
        self.confirm_import_button.setGeometry(QtCore.QRect(20, 160, 120, 30))
        self.confirm_import_button.setObjectName("confirm_import_button")
        self.confirm_import_button.setText("Confirm Import")

         # Add a QPushButton to delete data from pendrive
        self.delete_pendrive_button = QPushButton(self.centralwidget)
        self.delete_pendrive_button.setGeometry(QtCore.QRect(20, 160, 120, 30))
        self.delete_pendrive_button.setObjectName("delete_pendrive_button")
        self.delete_pendrive_button.setText("Clean pendrive")



        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        # Inside your Ui_MainWindow class, after creating UI elements, you can apply styles like this:
        self.centralwidget.setStyleSheet("""
    QPushButton {
        background-color: #007BFF;
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 5px;
    }

    QPushButton:hover {
        background-color: #0056b3;
    }

    QComboBox {
        background-color: white;
        color: #333;
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 2px 10px;
    }

    QTableWidget {
        background-color: white;
    }

    QLabel {
        font-size: 14px;
        font-weight: bold;
    }

    /* Add more styles for your other widgets as needed */

    /* Example styles for the pendrive import section */
    #import_pendrive_button {
        background-color: #28a745;
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 5px;
    }

    #import_pendrive_button:hover {
        background-color: #1e7e34;
    }

    #file_list_widget {
        background-color: #f8f9fa;
        border: 1px solid #ccc;
        border-radius: 5px;
    }

    #confirm_import_button {
        background-color: #ffc107;
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 5px;
    }

    #confirm_import_button:hover {
        background-color: #d39e00;
    }

    #delete_pendrive_button {
        background-color: #dc3545;
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 5px;
    }

    #delete_pendrive_button:hover {
        background-color: #bd2130;
    }
""")
        
        
        # Set the background color to black
        self.centralwidget.setStyleSheet("background-color: black;")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Item Manager"))
        self.import_button.setText(_translate("MainWindow", "Import Data"))
        self.backup_button.setText(_translate("MainWindow", "Backup Data"))
    
    

class ItemManagerApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
       # Initialize the database connection and cursor
        
         # Initialize the menu bar
        menubar = self.menuBar()

        # Create a "File" menu
        file_menu = menubar.addMenu("File")

        # Create "Open Database" action
        open_action = QAction("Open Database", self)
        open_action.triggered.connect(self.open_database)
        file_menu.addAction(open_action)

        # Create "Save Database" action
        save_action = QAction("Save Database", self)
        save_action.triggered.connect(self.save_database)
        file_menu.addAction(save_action)

        # Add a separator
        file_menu.addSeparator()

        # Create "Exit" action
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

          # Create a "Sales" menu
        sales_menu = menubar.addMenu("Sales")

        # Create a "Display Sales" action
        display_sales_action = QAction("Display Sales", self)
        display_sales_action.triggered.connect(self.display_sales_table)
        sales_menu.addAction(display_sales_action)
        
           # Add a separator
        sales_menu.addSeparator()


         # Connect the "Sales" menu item to the display_sales_table function
        sales_menu.aboutToShow.connect(self.display_sales_table)


        # Create a central widget for displaying sales
        self.sales_widget = QWidget(self)
        self.setCentralWidget(self.sales_widget)

        # Create a layout for the sales widget
        layout = QVBoxLayout()

        # Create a dropdown menu for selecting items
        self.item_combobox = QComboBox()
        layout.addWidget(self.item_combobox)

        # Create a table to display sales
        self.sales_table = QTableWidget()
        layout.addWidget(self.sales_table)

        # Set the layout for the sales widget
        self.sales_widget.setLayout(layout)

        # Initialize the item combobox and sales table
        self.load_items()
    def display_sales_table(self):
    #  Hide other components
        self.tableWidget.hide()
        self.import_button.hide()
        self.backup_button.hide()
        self.column_combobox.hide()
        self.total_weight_label.hide()
        self.delete_all_button.hide()
        self.import_pendrive_button.hide()
        self.file_list_widget.hide()
        self.confirm_import_button.hide()
        self.delete_pendrive_button.hide()

        # Show the sales-related components
        # You should create and display your sales-related table and dropdown menu here
        self.sales_table = QtWidgets.QTableWidget(self.centralwidget)
        self.sales_table.setGeometry(QtCore.QRect(160, 50, 620, 500))
        self.sales_table.setObjectName("sales_table")
        self.sales_table.setColumnCount(3)
        self.sales_table.setHorizontalHeaderLabels(["Item", "Quantity Sold", "Revenue"])

    # Create a QComboBox for selecting items
        self.sales_item_combobox = QComboBox(self.centralwidget)
        self.sales_item_combobox.setGeometry(QtCore.QRect(160, 10, 150, 30))
        self.sales_item_combobox.setObjectName("sales_item_combobox")
        self.sales_item_combobox.addItem("All Items")
    # You should populate the sales_item_combobox with your item list here

    # Connect the selection change event for the sales item dropdown
        self.sales_item_combobox.currentIndexChanged.connect(self.filter_sales_table)

    # Display the total revenue label
        self.sales_total_revenue_label = QLabel(self.centralwidget)
        self.sales_total_revenue_label.setGeometry(QtCore.QRect(160, 560, 300, 30))
        self.sales_total_revenue_label.setObjectName("sales_total_revenue_label")
        self.sales_total_revenue_label.setText("Total Revenue: ")

    # Connect the "Sales" button click event to the display_sales_table function
        self.sales_button.clicked.connect(self.display_sales_table)
    def open_database(self):
        options = QFileDialog.Options()
        db_file, _ = QFileDialog.getOpenFileName(
            self, "Open Database", "", "SQLite Database Files (*.db);;All Files (*)", options=options
        )

        if db_file:
            try:
                self.conn = sqlite3.connect(db_file)
                self.cursor = self.conn.cursor()
                self.load_items()
                self.update_table()
                self.update_total_weight()
            except Exception as e:
                print(f"Error while opening database: {str(e)}")

    def save_database(self):
        options = QFileDialog.Options()
        db_file, _ = QFileDialog.getSaveFileName(
            self, "Save Database", "", "SQLite Database Files (*.db);;All Files (*)", options=options
        )

        if db_file:
            try:
                shutil.copy("item_manager.db", db_file)
                print(f"Database saved to: {db_file}")
            except Exception as e:
                print(f"Error while saving database: {str(e)}")

    def load_items(self):
        # Load items from the database and populate the item combobox
        self.item_combobox.clear()
        self.cursor.execute("SELECT DISTINCT item FROM items")
        items = self.cursor.fetchall()
        all_items = [item[0] for item in items]
        self.item_combobox.addItems(all_items)

    def display_sales(self):
        # Get the selected item from the dropdown menu
        selected_item = self.item_combobox.currentText()

        # Clear the existing table
        self.sales_table.clear()

        # Fetch sales data from the database based on the selected item
        self.cursor.execute("SELECT * FROM sales WHERE item=?", (selected_item,))
        sales_data = self.cursor.fetchall()

        # Get the column names
        columns = [desc[0] for desc in self.cursor.description]

        # Set the column names as table headers
        self.sales_table.setColumnCount(len(columns))
        self.sales_table.setHorizontalHeaderLabels(columns)

        # Set the number of rows in the table
        self.sales_table.setRowCount(len(sales_data))

        # Populate the table with sales data
        for row_num, row_data in enumerate(sales_data):
            for col_num, col_data in enumerate(row_data):
                self.sales_table.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))

        
    # Rest of your ItemManagerApp methods...

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
        
        
        # Connect the "Delete All Data" button click event to the delete_all_data function
        self.delete_all_button.clicked.connect(self.delete_all_data)
        
         # Populate the item_combobox with all items
        self.load_items()
        # Create a function to update the table with loaded data
        self.update_table()

         # Connect the dropdown menu's selection change event
        self.column_combobox.currentIndexChanged.connect(self.filter_and_display)

        
        # Connect the "Import from Pendrive" button click event to the import_from_pendrive function
        self.import_pendrive_button.clicked.connect(self.import_from_pendrive)

        # Connect the "Confirm Import" button click event to the confirm_import function
        self.confirm_import_button.clicked.connect(self.confirm_import)
        
          # Connect the "Delete from Pendrive" button click event to the delete_from_pendrive function
        self.delete_pendrive_button.clicked.connect(self.delete_from_pendrive)

        # Initialize the total weight label

        # Initialize the total weight label
        self.update_total_weight()
    
    def import_from_pendrive(self):
        # Clear the file list widget
        self.file_list_widget.clear()

        # Search for relevant files on the pendrive
        pendrive_path = "/media/pi"  # Update this path to match your pendrive's mount point
        for root, dirs, files in os.walk(pendrive_path):
            for file in files:
                if file.endswith('.xlsx') or file.endswith('.csv'):
                    self.file_list_widget.addItem(file)

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
         # Search for relevant files on the pendrive
        pendrive_path = "/media/pi"  # Update this path to match your pendrive's mount point
        for root, dirs, files in os.walk(pendrive_path):
            for file in files:
                if file.endswith('.xlsx') or file.endswith('.csv'):
                    self.file_list_widget.addItem(file)

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

        # Update the total weight label
        self.update_total_weight()
    
    def update_total_weight(self):
        # Calculate and display the total weight
        total_weight = 0.0
        for row in range(self.tableWidget.rowCount()):
            weight_item = self.tableWidget.item(row, 2)  # Assuming weight is in the third column (index 2)
            if weight_item:
                total_weight += float(weight_item.text())
        self.total_weight_label.setText(f"Total Weight: {total_weight:.2f}")

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
       pass
   

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
    
    def confirm_import(self):
        # Get the selected file from the list widget
        selected_item = self.file_list_widget.currentItem()

        if selected_item:
            # Construct the full path to the selected file
            pendrive_path = "/media/pi"  # Update this path to match your pendrive's mount point
            file_path = os.path.join(pendrive_path, selected_item.text())

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

                    # Delete the file from the pendrive
                    os.remove(file_path)
                    print(f"Data imported and file '{selected_item.text()}' deleted from pendrive.")

            except Exception as e:
                print(f"Error while importing from {file_path}: {str(e)}")
    
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ItemManagerApp()
    window.show()
    sys.exit(app.exec_())