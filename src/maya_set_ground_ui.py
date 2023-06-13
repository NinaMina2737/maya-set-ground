#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import traceback

import maya.cmds as cmds
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
from PySide2 import QtCore, QtWidgets

import maya_set_ground as msg
reload(msg)

WINDOW_TITLE = "Set Ground"

class SetGroundUI(MayaQWidgetBaseMixin, QtWidgets.QWidget):
    """
    The UI class for the Set Ground tool.
    """
    def __init__(self):
        """
        Initializes the class.
        """
        super(self.__class__, self).__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.create_widget()
        self.create_layout()

    def create_widget(self):
        """
        Creates the widgets for the UI.
        """
        # Create the source widgets
        self.source_label = QtWidgets.QLabel("Source")

        self.source_object_label = QtWidgets.QLabel("Object")
        self.source_object_line_edit = QtWidgets.QLineEdit()
        self.source_object_line_edit.setReadOnly(True)

        self.source_components_label = QtWidgets.QLabel("Components")
        self.source_components_line_edit = QtWidgets.QLineEdit()
        self.source_components_line_edit.setReadOnly(True)

        self.source_vector_label = QtWidgets.QLabel("Vector")
        self.source_vector_line_edit = QtWidgets.QLineEdit()
        self.source_vector_line_edit.setReadOnly(True)

        self.source_selection_button = QtWidgets.QPushButton("Select Source")
        self.source_selection_button.clicked.connect(self.on_source_selection_button_clicked)

        # Create the target widgets
        self.target_label = QtWidgets.QLabel("Target")

        self.target_object_label = QtWidgets.QLabel("Object")
        self.target_object_line_edit = QtWidgets.QLineEdit()
        self.target_object_line_edit.setReadOnly(True)

        self.target_components_label = QtWidgets.QLabel("Components")
        self.target_components_line_edit = QtWidgets.QLineEdit()
        self.target_components_line_edit.setReadOnly(True)

        self.target_vector_label = QtWidgets.QLabel("Vector")
        self.target_vector_line_edit = QtWidgets.QLineEdit()
        self.target_vector_line_edit.setReadOnly(True)

        self.target_selection_button = QtWidgets.QPushButton("Select Target")
        self.target_selection_button.clicked.connect(self.on_target_selection_button_clicked)

        # Create the execute button
        self.execute_button = QtWidgets.QPushButton("Execute")
        self.execute_button.clicked.connect(self.on_execute_button_clicked)

    def create_layout(self):
        """
        Creates the layout for the UI.
        """
        main_layout = QtWidgets.QVBoxLayout()

        # Add the source widgets
        main_layout.addWidget(self.source_label)

        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.addWidget(self.source_object_label)
        horizontal_layout.addWidget(self.source_object_line_edit)
        main_layout.addLayout(horizontal_layout)

        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.addWidget(self.source_components_label)
        horizontal_layout.addWidget(self.source_components_line_edit)
        main_layout.addLayout(horizontal_layout)

        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.addWidget(self.source_vector_label)
        horizontal_layout.addWidget(self.source_vector_line_edit)
        main_layout.addLayout(horizontal_layout)

        main_layout.addWidget(self.source_selection_button)

        # Add a line
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        main_layout.addWidget(line)

        # Add the target widgets
        main_layout.addWidget(self.target_label)

        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.addWidget(self.target_object_label)
        horizontal_layout.addWidget(self.target_object_line_edit)
        main_layout.addLayout(horizontal_layout)

        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.addWidget(self.target_components_label)
        horizontal_layout.addWidget(self.target_components_line_edit)
        main_layout.addLayout(horizontal_layout)

        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.addWidget(self.target_vector_label)
        horizontal_layout.addWidget(self.target_vector_line_edit)
        main_layout.addLayout(horizontal_layout)

        main_layout.addWidget(self.target_selection_button)

        # Add a line
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        main_layout.addWidget(line)

        # Add the option to invert the target vector
        self.invert_target_vector_check_box = QtWidgets.QCheckBox("Invert Target Vector")
        self.invert_target_vector_check_box.setChecked(True)
        main_layout.addWidget(self.invert_target_vector_check_box)

        # Add a line
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        main_layout.addWidget(line)

        # Add the execute button
        main_layout.addWidget(self.execute_button)
        self.setLayout(main_layout)

    def on_source_selection_button_clicked(self):
        """
        Selects the source object.
        """
        # Get the selected object
        object_shape = cmds.ls(selection=True, objectsOnly=True)[0]
        object = cmds.listRelatives(object_shape, parent=True)[0]
        self.source_object = object
        self.source_object_line_edit.setText(object)

        # Get the selected components
        components = cmds.ls(selection=True, flatten=True)
        self.source_components_label.setText("Components ({0})".format(len(components)))
        self.source_components_line_edit.setText(str(components)[1:-1])

        # Get the normal of the selected object
        self.source_vector = msg.get_normal()
        self.source_vector_line_edit.setText(str(self.source_vector.elements)[1:-1])

    def on_target_selection_button_clicked(self):
        """
        Selects the target object.
        """
        # Get the selected object
        object_shape = cmds.ls(selection=True, objectsOnly=True)[0]
        object = cmds.listRelatives(object_shape, parent=True)[0]
        self.target_object = object
        self.target_object_line_edit.setText(object)

        # Get the selected components
        components = cmds.ls(selection=True, flatten=True)
        self.target_components_label.setText("Components ({0})".format(len(components)))
        self.target_components_line_edit.setText(str(components)[1:-1])

        # Get the normal of the selected object
        self.target_vector = msg.get_normal()
        self.target_vector_line_edit.setText(str(self.target_vector.elements)[1:-1])

    def on_execute_button_clicked(self):
        """
        Executes the Set Ground tool.
        """
        # Execute the tool
        # Check if the target vector should be inverted
        target_vector = self.target_vector
        if self.invert_target_vector_check_box.isChecked():
            target_vector = target_vector * -1
        msg.execute(object=self.source_object, source_normal=self.source_vector, target_normal=target_vector)

def execute():
    """
    Executes the UI.

    Raises:
        Exception: An error occurred.
    """
    try:
        # Check if the window already exists
        if cmds.window(WINDOW_TITLE, exists=True):
            cmds.deleteUI(WINDOW_TITLE)

        # Create the window
        window = SetGroundUI()
        window.show()
    except Exception as e:
        # Print the error message
        cmds.warning("An error occurred: {}".format(str(e)))
        # Print the traceback
        cmds.warning(traceback.format_exc())

if __name__ == "__main__":
    execute()
