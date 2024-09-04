from PyQt6.QtWidgets import (QApplication, QVBoxLayout,
                             QLabel, QWidget, QGridLayout,
                             QLineEdit, QPushButton, QComboBox,
                             QMessageBox)

import sys


class AverageSpeedCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Average Speed Calculator")

        grid = QGridLayout()

        distance_label = QLabel("Distance:")
        self.distance_line_edit = QLineEdit()

        time_label = QLabel("Time (hours):")
        self.time_line_edit = QLineEdit()

        calculate_button = QPushButton("Calculate")
        calculate_button.clicked.connect(self.calculate_speed)

        self.output_label = QLabel("")

        self.metric_system_combo = QComboBox()
        self.metric_system_combo.addItems(["Metric (km)", "Imperial (miles)"])

        grid.addWidget(distance_label, 0, 0)
        grid.addWidget(self.distance_line_edit, 0, 1)
        grid.addWidget(self.metric_system_combo, 0, 2)
        grid.addWidget(time_label, 1, 0)
        grid.addWidget(self.time_line_edit, 1, 1)
        grid.addWidget(calculate_button, 2, 1)
        grid.addWidget(self.output_label, 3, 0, 1, 3)

        self.setLayout(grid)

    def calculate_speed(self):
        try:
            if self.metric_system_combo.currentText() == "Metric (km)":
                avg_speed = (float(self.distance_line_edit.text())
                             / float(self.time_line_edit.text()))
                self.output_label.setText(f"Average Speed: {avg_speed} km/h")
            elif self.metric_system_combo.currentText() == "Imperial (miles)":
                avg_speed = (float(self.distance_line_edit.text())
                             / float(self.time_line_edit.text()))
                self.output_label.setText(f"Average Speed: {avg_speed} mph")
        except ValueError:
            err = QMessageBox()
            err.setText("Value Error")
            err.setInformativeText("There is a value error."
                                   " Please enter values for distance and time")
            err.setWindowTitle("Error")
            err.exec()
        except ZeroDivisionError:
            err = QMessageBox()
            err.setText("Zero Division Error")
            err.setInformativeText("Please enter non zero values for time")
            err.setWindowTitle("Error")
            err.exec()


app = QApplication(sys.argv)
speed_calculator = AverageSpeedCalculator()
speed_calculator.show()
sys.exit(app.exec())


