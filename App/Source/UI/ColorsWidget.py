from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Source.Tools import Tools
from Source.UI.CanvasWidget import Canvas
from Source.Utils import *

COLORS = [
    '#ffffff', '#010000', '#ff0000', '#0000ff', '#00ff00', '#ffff00', '#00ffff', '#ff00ff',
    '#c0c0c0', '#404040', '#800000', '#000080', '#008000', '#ff4500', '#008080', '#9400d3'
]


class ColorsWidget(QWidget):
    """
    This class will hold the colors and the color picker window.
    """

    def __init__(self, canvas: Canvas):
        """
       Class constructor.

       :param canvas: the canvas to bind it to the buttons in order to change the pen color
       """

        super(ColorsWidget, self).__init__()

        self.layout = QHBoxLayout()

        self.main_frame = QFrame()
        self.main_frame_layout = QGridLayout()

        self.canvas = canvas

        self.setup()

    def setup(self) -> None:
        """
        Function used to initialize the entire widget, set variables or add another widgets to it.

        :return: None
        """

        # Setup the main widget
        self.setObjectName("colors_widget")
        self.setFixedSize(QSize(420, 110))
        self.installEventFilter(self)
        self.setLayout(self.layout)
        self.layout.addWidget(self.main_frame)

        # Setup the main frame
        self.main_frame.setObjectName("main_frame")
        self.main_frame.setLayout(self.main_frame_layout)
        self.main_frame.setStyleSheet(css(
            f"QWidget#{self.main_frame.objectName()}",
            "border-style: solid",
            "border-width: 1px",
            f"border-color: {COLOR}",
            "border-radius: 3px",
            f"background-color: {BACKGROUND_DARK}"
        ))

        # Add the buttons to layout
        for i, color in zip(range(len(COLORS)), COLORS):
            self.main_frame_layout.addWidget(ColorButton(self.canvas, color, i), int(i / 8), i % 8)
        self.main_frame_layout.addWidget(ColorPickerButton(self.canvas), 0, 8, 2, 1)

    def change_color(self, color: QColor) -> None:
        """
        Function used to call the function from canvas in order to change the pen color.

        :param color: the hex value of the color
        :return: None
        """

        if self.canvas.get_tool() == Tools.ERASER:
            self.canvas.set_tool(Tools.PEN)
        self.canvas.set_pen_color(color)

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
                f"border-color: {COLOR_HOVER}",
                "border-radius: 3px",
                f"background-color: {BACKGROUND_DARK}"
            ))
            return True

        # Check if cursor left the widget
        elif event.type() == QEvent.Leave:
            self.main_frame.setStyleSheet(css(
                f"QWidget#{self.main_frame.objectName()}",
                "border-style: solid",
                "border-width: 1px",
                f"border-color: {COLOR}",
                "border-radius: 3px",
                f"background-color: {BACKGROUND_DARK}"
            ))
            return True

        return False


class ColorButton(QPushButton):
    """
    This class creates buttons with a specific color, when clicked it will change the pen color on the canvas.
    """

    def __init__(self, canvas: Canvas, color: str, number: int):
        """
        Class constructor.

        :param canvas: the canvas to bind it to the button in order to change the pen color
        :param color: the color that is used to change the button's background and to set the pen color to the canvas
        :return: None
        """

        super(ColorButton, self).__init__()

        self.canvas = canvas

        self.color = color
        self.number = number

        self.setup()

    def setup(self) -> None:
        """
        Function used to initialize the entire widget, set variables or generate add another widgets to it.

        :return: None
        """

        # Setup the button
        self.setObjectName(f"color_button_{self.number}")
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFixedSize(QSize(25, 25))
        self.pressed.connect(lambda: self.canvas.set_pen_color(self.color))
        self.setStyleSheet(merge_css(
            css(
                f"QPushButton#{self.objectName()}",
                f"background-color: {self.color}",
                "border-style: solid",
                "border-width: 1px",
                "border-radius: 3px",
                f"border-color: {COLOR}",
            ),
            css(
                f"QPushButton#{self.objectName()}:hover",
                f"border-color: {COLOR_HOVER}",
            )
        ))


class ColorPickerButton(QPushButton):
    """
    This class opens a color picker window.
    """

    def __init__(self, canvas: Canvas):
        """
        Class constructor.

        :param canvas: the canvas to bind it to the buttons in order to change the pen color
        """

        super(ColorPickerButton, self).__init__()

        self.canvas = canvas

        self.color = "#000000"

        self.setup()

    def setup(self) -> None:
        """
        Function used to initialize the entire widget, set variables or generate add another widgets to it.

        :return: None
        """

        # Setup the button
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setObjectName(f"color_picker_button")
        self.setFixedSize(QSize(59, 59))
        self.setIcon(QIcon("../Resources/rainbow.png"))
        self.setIconSize(QSize(57, 57))
        self.pressed.connect(lambda: self.pick_color())
        self.setStyleSheet(merge_css(
            css(
                f"QPushButton#{self.objectName()}",
                "border-style: solid",
                "border-width: 1px",
                "border-radius: 3px",
                f"border-color: {COLOR}",
            ),
            css(
                f"QPushButton#{self.objectName()}:hover",
                f"border-color: {COLOR_HOVER}",
            )
        ))

    def pick_color(self) -> None:
        """
        Function used to start a color dialog pup-up to choose a color and then call change_color function.

        :return: None
        """

        self.color = QColorDialog.getColor()

        if self.color.isValid():
            self.canvas.set_pen_color(self.color.name())
