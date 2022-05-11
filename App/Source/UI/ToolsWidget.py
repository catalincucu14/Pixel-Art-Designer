from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import *

from Source.Tools import Tools
from Source.UI.CanvasWidget import Canvas
from Source.Utils import *


class ToolsWidget(QWidget):
    """
    This class will hold all buttons for changing the tool used to draw.
    Every button will change the tool in Canvas nothing more.
    """

    def __init__(self, canvas: Canvas):
        """
        Class constructor.

        :param canvas: the canvas widget to bind it to the buttons
        """

        super(ToolsWidget, self).__init__()

        self.layout = QHBoxLayout()

        self.main_frame = QFrame()
        self.main_frame_layout = QHBoxLayout()

        self.pen_size = QComboBox()

        self.canvas = canvas

        self.setup()

    def setup(self) -> None:
        """
        Function used to initialize the entire widget, set variables or add another widgets to it.

        :return: None
        """

        # Setup the main widget
        self.setObjectName("tools_widget")
        self.setFixedHeight(110)
        self.installEventFilter(self)
        self.setLayout(self.layout)
        self.layout.addWidget(self.main_frame)

        # Setup the main frame
        self.main_frame.setObjectName("main_frame")
        self.main_frame.setLayout(self.main_frame_layout)
        self.main_frame_layout.setSpacing(25)
        self.main_frame_layout.setContentsMargins(25, 0, 25, 0)
        self.main_frame.setStyleSheet(css(
            f"QWidget#{self.main_frame.objectName()}",
            "border-style: solid",
            "border-width: 1px",
            f"border-color: {COLOR}",
            "border-radius: 3px",
            f"background-color: {BACKGROUND_DARK}"
        ))

        # Setup the combobox
        self.pen_size.setObjectName("pen_size_combobox")
        for i in range(10):
            self.pen_size.addItem(str(i + 1))
        self.pen_size.currentTextChanged.connect(self.change_pen_size)
        self.pen_size.setEditable(True)
        self.pen_size.setStyleSheet(merge_css(
            css(
                f"QComboBox#{self.pen_size.objectName()}",
                "border-style: solid",
                "border-width: 1px",
                f"border-color: {COLOR}",
                "border-radius: 0px",
                "width: 59px",
                "height: 30px",
                "font-size: 20px",
                f"color: {COLOR}",
                f"background-color: rgba(153, 170, 181, 0.1)"
            ),
            css(
                f"QComboBox#{self.pen_size.objectName()}:hover, QComboBox#{self.pen_size.objectName()}:on",
                f"border-color: {COLOR_HOVER}",
                "background-color: rgba(64, 78, 237, 0.1)"
            ),
            css(
                f"QComboBox#{self.pen_size.objectName()} QListView",
                "outline: none",
                f"background-color: {BACKGROUND}",
                f"color: {COLOR}",
                f"selection-background-color: {BACKGROUND_DARK}",
                f"selection-color: {COLOR_HOVER}",
            )))

        # Add the buttons to main frame
        self.main_frame_layout.addWidget(self.pen_size)
        self.main_frame_layout.addWidget(ToolButton(self, Tools.PICKER))
        self.main_frame_layout.addWidget(ToolButton(self, Tools.FILL))
        self.main_frame_layout.addWidget(ToolButton(self, Tools.BRUSH))
        self.main_frame_layout.addWidget(ToolButton(self, Tools.CIRCLE))
        self.main_frame_layout.addWidget(ToolButton(self, Tools.SQUARE))
        self.main_frame_layout.addWidget(ToolButton(self, Tools.LINE))
        self.main_frame_layout.addWidget(ToolButton(self, Tools.ERASER))
        self.main_frame_layout.addWidget(ToolButton(self, Tools.PEN))

        # Make the widget fit its content
        self.setFixedWidth(self.main_frame_layout.sizeHint().width())

    def change_pen_size(self, value: str) -> None:
        """
        Function used to change the pen size used to draw on canvas.

        :param value: the value from combobox
        :return: None
        """

        if not value:
            return

        if int(value) > 10:
            self.pen_size.setCurrentIndex(0)
            return

        self.canvas.set_pen_size(value)

    def change_tool(self, tool: Tools) -> None:
        """
        Function used to change the tool used to draw on canvas.

        :param tool: the tool type
        :return: None
        """

        self.canvas.set_tool(tool)

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
                "QWidget#main_frame",
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
                "QWidget#main_frame",
                "border-style: solid",
                "border-width: 1px",
                f"border-color: {COLOR}",
                "border-radius: 3px",
                f"background-color: {BACKGROUND_DARK}"
            ))
            return True

        return False


class ToolButton(QPushButton):
    """
    This class makes custom buttons for changing the tool used to draw
    It has a dummy switch for assigning the too to change as well as the icon.
    """

    def __init__(self, tools_widget: ToolsWidget, tool: Tools):
        """
        Class constructor.

        :param tools_widget: the widget that will create an instance of this button
        :param tool: the button type that gives the functionality
        """

        super(ToolButton, self).__init__()

        self.tool_widget = tools_widget

        self.tool = tool

        self.icon = ""
        self.icon_size = None

        self.setup()

    def setup(self) -> None:
        """
        Function used to initialize the entire widget, set variables or add another widgets to it.

        :return: None
        """

        # Change the cursor shape
        self.setCursor(QCursor(Qt.PointingHandCursor))

        # Enable hover events
        self.installEventFilter(self)

        # Set the button dimension
        self.setFixedSize(QSize(59, 59))

        # Change icon and the functionality based on what type of button it will be created
        if self.tool == Tools.PEN:
            self.setObjectName("pen_button")
            self.icon = "../Resources/tools/pen"
            self.setToolTip("PEN")

        elif self.tool == Tools.ERASER:
            self.setObjectName("eraser_button")
            self.icon = "../Resources/tools/eraser"
            self.setToolTip("ERASER")

        elif self.tool == Tools.LINE:
            self.setObjectName("line_button")
            self.icon = "../Resources/tools/line"
            self.setToolTip("LINE")

        elif self.tool == Tools.SQUARE:
            self.setObjectName("square_button")
            self.icon = "../Resources/tools/square"
            self.setToolTip("SQUARE")

        elif self.tool == Tools.CIRCLE:
            self.setObjectName("circle_button")
            self.icon = "../Resources/tools/circle"
            self.setToolTip("CIRCLE")

        elif self.tool == Tools.BRUSH:
            self.setObjectName("text_button")
            self.icon = "../Resources/tools/brush"
            self.setToolTip("BRUSH")

        elif self.tool == Tools.FILL:
            self.setObjectName("fill_button")
            self.icon = "../Resources/tools/fill"
            self.setToolTip("FILL")

        elif self.tool == Tools.PICKER:
            self.setObjectName("picker_button")
            self.icon = "../Resources/tools/picker"
            self.setToolTip("COLOR PICKER")

        # Assign a function to the button to change the toon in canvas
        self.pressed.connect(lambda t=self.tool: self.tool_widget.change_tool(t))

        # Set the size of the icon
        self.icon_size = QSize(45, 45)

        # Set the button style
        self.setStyleSheet(merge_css(
            css(
                f"QPushButton#{self.objectName()}",
                "border-style: solid",
                "border-width: 1px",
                f"border-color: {COLOR}",
                "border-radius: 3px",
                f"qproperty-icon: url(\"{self.icon}.png\")",
                "background-color: rgba(153, 170, 181, 0.1)"
            ),
            css(
                f"QPushButton#{self.objectName()}:hover",
                f"border-color: {COLOR_HOVER}",
                "background-color: rgba(64, 78, 237, 0.1)"
            )))

        # Set the icon size
        self.setIconSize(self.icon_size)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        """
        Function used to change the icon when is hovered.

        :param obj: the object
        :param event: the event
        :return: True or False if the events we wanted have occurred
        """

        # Check if the cursor is on the widget
        if event.type() == QEvent.Enter:
            self.setIcon(QIcon(f"{self.icon}_hover.png"))
            return True

        # Check if cursor left the widget
        elif event.type() == QEvent.Leave:
            self.setIcon(QIcon(f"{self.icon}.png"))
            return True

        return False
