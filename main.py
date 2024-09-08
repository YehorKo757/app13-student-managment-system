from PyQt6.QtWidgets import (QApplication, QVBoxLayout,
                             QLabel, QWidget, QGridLayout,
                             QLineEdit, QPushButton, QMainWindow,
                             QTableWidget, QTableWidgetItem, QDialog,
                             QComboBox, QToolBar, QStatusBar, QMessageBox)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import QSettings, QByteArray, Qt
import sqlite3
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        # Window minimum size
        self.setMinimumSize(800, 600)

        # Window position (px from left upper corner)
        self.move(50, 50)

        # Set settings and read settings
        self.settings = QSettings("Name of company", "Name of app")
        self.read_settings()

        # add a Menu bar
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.about)
        help_menu_item.addAction(about_action)

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        # add a Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("id",
                                              "Name",
                                              "Course",
                                              "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Create toolbar and add elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Create status bar and add status elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)

        # Detect when no cell selected
        self.table.itemSelectionChanged.connect(self.cell_unselected)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def cell_unselected(self):
        if not self.table.selectedItems():
            children = self.findChildren(QPushButton)
            if children:
                for child in children:
                    self.statusbar.removeWidget(child)

    def closeEvent(self, event):
        self.write_settings()
        super().closeEvent(event)
        event.accept()

    def write_settings(self):
        self.settings.setValue("geometry",
                               self.saveGeometry())
        self.settings.setValue("windowState",
                               self.saveState())

    def read_settings(self):
        self.restoreGeometry(self.settings.value("geometry",
                                                 QByteArray()))
        self.restoreState(self.settings.value("windowState",
                                              QByteArray()))

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number,
                                   column_number,
                                   QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        self.dialog_insert = InsertDialog()
        self.dialog_insert.exec()

    def search(self):
        self.dialog_search = SearchDialog()
        self.dialog_search.exec()

    def edit(self):
        self.dialog_edit = EditDialog()
        self.dialog_edit.exec()

    def delete(self):
        self.dialog_delete = DeleteDialog()
        self.dialog_delete.exec()

    def about(self):
        self.dialog_about = AboutDialog()
        self.dialog_about.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        This app was created during the course "The Python Mega Course".
        Feel free to modify and reuse this app.
        """
        self.setText(content)


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()

        # Add student_name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add combo box of courses
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add mobile widget
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile Number")
        layout.addWidget(self.mobile)

        # Add a submit button
        button = QPushButton("Register")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile)"
                       " VALUES (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        student_management.load_data()
        student_management.dialog_insert.close()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()

        # Add student_name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add a submit button
        button = QPushButton("Search")
        button.clicked.connect(self.search_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def search_student(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?",
                                (name,))
        rows = list(result)
        items = student_management.table.findItems(name,
                                                   Qt.MatchFlag.MatchFixedString)
        for item in items:
            student_management.table.item(item.row(),
                                          1).setSelected(True)

        cursor.close()
        connection.close()
        student_management.dialog_search.close()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Student Data")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()

        index = student_management.table.currentRow()
        student_name = student_management.table.item(index, 1).text()
        student_course = student_management.table.item(index, 2).text()
        student_mobile = student_management.table.item(index, 3).text()
        self.student_id = student_management.table.item(index, 0).text()

        # Add student_name widget
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add combo box of courses
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(student_course)
        layout.addWidget(self.course_name)

        # Add mobile widget
        self.mobile = QLineEdit(student_mobile)
        self.mobile.setPlaceholderText("Mobile Number")
        layout.addWidget(self.mobile)

        # Add a submit button
        button = QPushButton("Submit")
        button.clicked.connect(self.edit_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def edit_student(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (self.student_name.text(),
                        self.course_name.itemText(self.course_name.currentIndex()),
                        self.mobile.text(),
                        self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        student_management.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Student Data")

        layout = QGridLayout()

        confirmation_message = QLabel("Are you sure you want to delete?")
        yes_button = QPushButton("Yes")
        no_button = QPushButton("No")

        layout.addWidget(confirmation_message, 0, 0, 1, 2)
        layout.addWidget(yes_button, 1, 0)
        layout.addWidget(no_button, 1, 1)
        self.setLayout(layout)

        yes_button.clicked.connect(self.delete_student)
        no_button.clicked.connect(self.no_button)

    def delete_student(self):
        index = student_management.table.currentRow()
        student_id = student_management.table.item(index,
                                                        0).text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE from students WHERE id = ?",
                       (student_id,))
        connection.commit()
        cursor.close()
        connection.close()
        student_management.load_data()
        student_management.dialog_delete.close()  # or self.close

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was deleted successfully!")
        confirmation_widget.exec()

    def no_button(self):
        self.close()


app = QApplication(sys.argv)
student_management = MainWindow()
student_management.show()
student_management.load_data()
sys.exit(app.exec())
