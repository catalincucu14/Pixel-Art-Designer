from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Source import Utils
from Source.Tools import Tools
from Source.Utils import *

TOOLS = {
    Tools.PEN: "pen",
    Tools.ERASER: "eraser",
    Tools.LINE: "line",
    Tools.SQUARE: "square",
    Tools.CIRCLE: "circle",
    Tools.BRUSH: "text",
    Tools.FILL: "fill",
    Tools.PICKER: "picker"

}


class StatusWidget(QWidget):
    def __init__(self):
        """
       Class constructor.

       """

        super(StatusWidget, self).__init__()

        self.layout = QHBoxLayout()

        self.main_frame = QFrame()
        self.main_frame_layout = QHBoxLayout()

        self.canvas_width = 500
        self.canvas_height = 250
        self.tool = Tools.PEN
        self.pos_x = "000"
        self.pos_y = "000"
        self.zoom = "0.00"
        self.position_label = QLabel(f"ZOOM: {self.zoom} | POSITION: X: {self.pos_x} Y: {self.pos_y}")
        self.color_label = QLabel(f"000000")
        self.tool_label = QLabel(
            f"SIZE: {self.canvas_width}X{self.canvas_height} | SELECTED TOOL: {TOOLS.get(self.tool).upper()}")

        self.setup()

    def setup(self) -> None:
        """
        Function used to initialize the entire widget, set variables or add another widgets to it.

        :return: None
        """

        # Setup the main widget
        self.setObjectName("status_widget")
        self.setFixedHeight(50)
        self.installEventFilter(self)
        self.setLayout(self.layout)

        # Setup the layout
        self.layout.addWidget(self.main_frame)
        self.layout.setContentsMargins(10, 5, 5, 10)

        # Setup the main frame
        self.main_frame.setObjectName("main_frame")
        self.main_frame.setLayout(self.main_frame_layout)
        self.main_frame.setStyleSheet(css(
            f"QWidget#{self.main_frame.objectName()}",
            "border-style: solid",
            "border-width: 1px",
            f"border-color: {Utils.COLOR}",
            "border-radius: 3px",
            "background-color: #23272A"
        ))

        # Add the labels to main frame
        self.main_frame_layout.addWidget(self.tool_label)
        self.main_frame_layout.addWidget(self.color_label)
        self.main_frame_layout.addWidget(self.position_label)

        # Set the style and properties to the labels
        self.tool_label.setObjectName("status_tool_label")
        self.color_label.setObjectName("status_color_label")
        self.position_label.setObjectName("status_position_label")

        # Set the alignment to the labels
        self.tool_label.setAlignment(Qt.AlignLeft)
        self.color_label.setAlignment(Qt.AlignCenter)
        self.position_label.setAlignment(Qt.AlignRight)

        # Enable the interaction with the color label if someone wants to copy it
        self.color_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        # Set the style to the labels
        css_temp = merge_css(
            css(
                f"QLabel#{self.tool_label.objectName()}, QLabel#{self.position_label.objectName()}",
                "font-size: 13px",
                f"color: {Utils.COLOR}"
            ),
            css(
                f"QLabel#{self.tool_label.objectName()}:hover, QLabel#{self.position_label.objectName()}:hover",
                "font-size: 13px",
                f"color: {Utils.COLOR_HOVER}"
            ))
        self.tool_label.setStyleSheet(css_temp)
        self.position_label.setStyleSheet(css_temp)
        self.color_label.setStyleSheet(css(
            f"QLabel#{self.color_label.objectName()}",
            f"color: #000000",
            "font-size: 15px",
            "font-weight: bold"
        ))

    def set_position_and_zoom(self, x: int = None, y: int = None, zoom: float = None) -> None:
        """
        Function used to update the zoom and the mouse position on canvas.
        This function will be called in 2 different ways.
        To update the position or the zoom so that's why are defaults None.

        :param x: the position on x axis
        :param y: the position on y axis
        :param zoom: the zoom of the original canvas
        :return: None
        """

        # Update the position
        if x is not None and y is not None:
            self.pos_x = ("00" + str(x))[-3:]
            self.pos_y = ("00" + str(y))[-3:]

        # Update the zoom
        if zoom is not None:
            self.zoom = (str(round(zoom, 2)) + "0")[:4]

        # Update the label
        self.position_label.setText(f"ZOOM: {self.zoom} | POSITION: X: {self.pos_x} Y: {self.pos_y}")

    def set_dimensions_and_tool(self, width: int = None, height: int = None, tool: Tools = None) -> None:
        """
        Function used to change the tool used in the label.
        This function will be called in 2 different ways.
        To update the dimensions of the canvas or the tools used so that's why are defaults None.

        :param width: canvas width
        :param height: canvas height
        :param tool: the tool used
        :return: None
        """

        # Update the dimensions
        if width is not None and height is not None:
            self.canvas_width = width
            self.canvas_height = height

        # Update the tool
        if tool is not None:
            self.tool = tool

        # Change the label
        self.tool_label.setText(
            f"SIZE: {self.canvas_width} X {self.canvas_height} | SELECTED TOOL: {TOOLS.get(self.tool).upper()}")

    def set_color(self, color: str) -> None:

        # Set the hex value of the color to the label
        self.color_label.setText(f"{color[1:].upper()}")

        # Change the font color to match the color used to draw
        self.color_label.setStyleSheet(css(
            f"QLabel#{self.color_label.objectName()}",
            f"color: {color}",
            "font-size: 15px",
            "font-weight: bold"
        ))

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        """
        Function used to change the css when is hovered.

        :param obj: the object
        :param event: the event
        :return: True or False if the events we wanted have occurred
        """

        # Check if the cursor is above the widget
        if event.type() == QEvent.Enter:
            self.main_frame.setStyleSheet(css(
                f"QWidget#{self.main_frame.objectName()}",
                "border-style: solid",
                "border-width: 1px",
                f"border-color: {Utils.COLOR_HOVER}",
                "border-radius: 3px",
                "background-color: #23272A"
            ))
            return True

        # Check if cursor left the widget
        elif event.type() == QEvent.Leave:
            self.main_frame.setStyleSheet(css(
                f"QWidget#{self.main_frame.objectName()}",
                "border-style: solid",
                "border-width: 1px",
                f"border-color: {Utils.COLOR}",
                "border-radius: 3px",
                "background-color: #23272A"
            ))
            return True

        return False
