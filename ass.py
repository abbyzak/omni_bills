import os
import sys
import time

from omni_runnner import *
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtGui import QFont

def new():
  # Open the input file for reading
  with open("bills.txt", "r") as input_file:
    # Read the input file line by line
    lines = input_file.readlines()

  # Check if the input file has at least 25 lines
  if len(lines) >= 25:
    # Keep track of the current output file number
    file_number = 1

    # Create the first output file
    output_file = open("{}.txt".format(file_number), "w")

    # Iterate over the lines in the input file
    for line in lines:
      # Write the line to the current output file
      output_file.write(line)

      # If the current output file has 25 lines, close it and open a new one
      if output_file.tell() >= 25*len(line):
        output_file.close()
        file_number += 1
        output_file = open("{}.txt".format(file_number), "w")

    # Close the last output file
    output_file.close()
  else:
    # The input file does not have enough lines, so print an error message
    print("Error: The input file must have at least 25 lines.")



class TextViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Text Viewer')

        # Create a label to Process the text
        self.label = QLabel()
        self.label.setFont(QFont('Arial', 15))

        # Create an input box to enter the file name
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText('Enter file name')

        # Create a button to trigger the Process of the text
        self.button = QPushButton('Process Single File')
        self.button2 = QPushButton('Process Bill.txt')
        self.button.clicked.connect(self.Process_text)
        self.button2.clicked.connect(new)

        # Create a vertical layout to hold the widgets
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input_box)
        layout.addWidget(self.button)
        layout.addWidget(self.button2)
        self.setLayout(layout)

    def Process_text(self):
        # Get the file name from the input box
        file_name = self.input_box.text()

        # Open the file and read its content
        with open(file_name, 'r') as file:
            text = file.read()

        # Set the label's text to the content of the file
        self.label.setText(text)
        doit(file_name)
        os.remove(file_name)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = TextViewer()
    viewer.show()
    sys.exit(app.exec_())
