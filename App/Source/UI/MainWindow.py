from PyQt5.QtWidgets import *

from Source.UI.CanvasWidget import CanvasWidget
from Source.UI.ColorsWidget import ColorsWidget
from Source.UI.SettingsWidget import SettingsWidget
from Source.UI.StatusWidget import StatusWidget
from Source.UI.ToolsWidget import ToolsWidget
from Source.Utils import *


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        """
        Class constructor.

        """

        super().__init__()

        self.main_widget = QWidget()

        self.layout = QGridLayout()

        self.status_widget = StatusWidget()
        self.canvas_widget = CanvasWidget(self.status_widget)
        self.tools_widget = ToolsWidget(self.canvas_widget.canvas)
        self.settings_widget = SettingsWidget(self.canvas_widget)
        self.colors_widget = ColorsWidget(self.canvas_widget.canvas)

        self.setup()

    def setup(self) -> None:
        """
        Function used to initialize the entire widget, set variables or add another widgets to it.

        :return: None
        """

        # Set the main widget to the interface
        self.setCentralWidget(self.main_widget)

        # Set the name of the main window
        self.setWindowTitle("Pixel Art Designer")
        self.setObjectName("pixel_art_designer")

        # Set the geometry but I don't know how it really works
        self.setGeometry(1280, 720, 1920, 1010)

        # Set the main window to start maximized
        self.showMaximized()

        # Set the layout of the widget
        self.main_widget.setLayout(self.layout)

        # Add the 4 widgets that will be shown in the main widget to layout
        self.layout.addWidget(self.settings_widget, 0, 0)
        self.layout.addWidget(self.tools_widget, 0, 1)
        self.layout.addWidget(self.colors_widget, 0, 2)
        self.layout.addWidget(self.canvas_widget, 1, 0, 1, 3)
        self.layout.addWidget(self.status_widget, 2, 0, 1, 3)

        # Set the style
        self.setStyleSheet(css(
            f"QMainWindow#{self.objectName()}",
            F"background-color: {BACKGROUND}"
        ))
