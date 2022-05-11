import re

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Source.Settings import Settings
from Source.UI.CanvasWidget import CanvasWidget
from Source.Utils import *


class SettingsWidget(QWidget):
    """
    This class will hold all buttons for canvas saving, canvas clear, new canvas etc.
    """

    def __init__(self, canvas_widget: CanvasWidget):
        """
        Class constructor.

        :param canvas_widget: the canvas widget to bind it to the buttons
        """

        super(SettingsWidget, self).__init__()

        self.layout = QHBoxLayout()

        self.main_frame = QFrame()
        self.main_frame_layout = QGridLayout()

        self.save_canvas_button = SettingButton(self, Settings.SAVE)
        self.open_canvas_button = SettingButton(self, Settings.OPEN)
        self.new_canvas_button = SettingButton(self, Settings.NEW)
        self.clear_canvas_button = SettingButton(self, Settings.CLEAR)
        self.undo_button = SettingButton(self, Settings.UNDO)
        self.redo_button = SettingButton(self, Settings.REDO)

        self.canvas_widget = canvas_widget

        self.setup()

    def setup(self) -> None:
        """
        Function used to initialize the entire widget, set variables or add another widgets to it.

        :return: None
        """

        # Setup the main widget
        self.setObjectName("settings_widget")
        self.setFixedSize(QSize(420, 110))
        self.setLayout(self.layout)
        self.installEventFilter(self)
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

        # Add the buttons to main frame
        self.main_frame_layout.addWidget(self.save_canvas_button, 0, 0, 2, 1)
        self.main_frame_layout.addWidget(self.open_canvas_button, 0, 1, 2, 1)
        self.main_frame_layout.addWidget(self.new_canvas_button, 0, 2, 2, 1)
        self.main_frame_layout.addWidget(self.clear_canvas_button, 0, 3, 2, 1)
        self.main_frame_layout.addWidget(self.redo_button, 0, 4)
        self.main_frame_layout.addWidget(self.undo_button, 1, 4)

    def new_canvas(self) -> None:
        """
        Function used to launch an input pop-up to get the dimensions to create a new canvas.

        :return: None
        """

        # Create the pop-up and start it
        new_canvas = NewCanvasDialog(self.canvas_widget)
        new_canvas.exec_()

    def save_canvas(self) -> None:
        """
        Function used to launch a file dialog to choose the path where the image will be saved.
        It will check if the file name si correct.

        :return: None
        """

        # Open the file dialog window to choose the path
        path, _ = QFileDialog.getSaveFileName(self, "Save Image", "image", "Images (*.png)")

        # If the path is null (most likely because the dialog window was closed) just return
        if path == "":
            return

        # Add the .png extensions if is not
        if not path.__contains__(".png"):
            path = path + ".png"

        # Check if the file name is correct (it doesn't contains slash or something similar)
        if re.match(r"([a-zA-Z0-9\s_\\.\-\(\):])+(.png)$", re.split(r"/|\\", path)[-1]):
            # Call the function from canvas widget to save the canvas to the specified path
            self.canvas_widget.save_canvas(path)

    def clear_canvas(self) -> None:
        """
        Function used to launch a confirmation pop-up to confirm the canvas clearance.

        :return: None
        """

        # Create the pop-up and start it
        clear_canvas = ClearCanvasDialog(self.canvas_widget)
        clear_canvas.exec_()

    def open_canvas(self) -> None:
        """
        Function used to launch a file dialog to choose an image to be opened.
        Then create the canvas, alpha channel and the grid with the new dimensions.
        Canvas's pixmap it will be image's one.
        If the image doesn't match the limits resize it.

        :return: None
        """

        # Open the file dialog window to choose the image
        path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg)")

        # If the path is null (most likely because the dialog window was closed) just return
        if path == "":
            return

        # Open the image in a pixmap
        pixmap = QPixmap(path)

        # Get the dimensions
        width = pixmap.size().width()
        height = pixmap.size().height()

        # Check if the image matches the limits
        if not 50 <= width <= 500 and not 50 <= height <= 250:
            # If is smaller, resize it to the closest inferior limit
            if width < 50 or height < 50:
                pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio)
            # If is bigger, resize it to the closest superior limit
            if width > 500 or height > 250:
                pixmap = pixmap.scaled(500, 250, Qt.KeepAspectRatio)

        # Update dimensions
        width = pixmap.size().width()
        height = pixmap.size().height()

        # Resize the scene
        self.canvas_widget.scene.setSceneRect(0, 0, width, height)

        # Call the function from canvas widget to create again the canvas with the new dimensions and a new image
        self.canvas_widget.new_canvas(width, height, pixmap)

    def undo_canvas(self) -> None:
        """
        Function used to undo a modification on the canvas.
        It still doesn't work.

        :return: None
        """

        self.canvas_widget.undo()

    def redo_canvas(self) -> None:
        """
        Function used to redo a modification on the canvas.
        It still doesn't work.

        :return: None
        """

        self.canvas_widget.redo()

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


class SettingButton(QPushButton):
    """
    This class makes custom buttons for executing certain things like saving the canvas.
    It has a dummy switch for assigning the task as well as the icon.
    """

    def __init__(self, setting_widget: SettingsWidget, action_type: Settings):
        """
        Class constructor.

        :param setting_widget: the widget that will create an instance of this button
        :param action_type: the button type that gives the functionality
        """

        super(SettingButton, self).__init__()

        self.setting_widget = setting_widget

        self.type = action_type

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

        # Change icon and the functionality based on what type of button it will be created
        if self.type == Settings.SAVE:
            self.setObjectName("save_canvas_button")
            self.setFixedSize(QSize(59, 59))
            self.icon = "../Resources/settings/save"
            self.icon_size = QSize(45, 45)
            self.setToolTip("SAVE CANVAS")
            self.pressed.connect(lambda: self.setting_widget.save_canvas())

        elif self.type == Settings.CLEAR:
            self.setObjectName("clear_canvas_button")
            self.setFixedSize(QSize(59, 59))
            self.icon = "../Resources/settings/clear"
            self.icon_size = QSize(45, 45)
            self.setToolTip("CLEAR CANVAS")
            self.pressed.connect(lambda: self.setting_widget.clear_canvas())

        elif self.type == Settings.NEW:
            self.setObjectName("new_canvas_button")
            self.setFixedSize(QSize(59, 59))
            self.icon = "../Resources/settings/new"
            self.icon_size = QSize(45, 45)
            self.setToolTip("NEW CANVAS")
            self.pressed.connect(lambda: self.setting_widget.new_canvas())

        elif self.type == Settings.OPEN:
            self.setObjectName("open_canvas_button")
            self.setFixedSize(QSize(59, 59))
            self.icon = "../Resources/settings/open"
            self.icon_size = QSize(45, 45)
            self.setToolTip("OPEN IMAGE")
            self.pressed.connect(lambda: self.setting_widget.open_canvas())

        elif self.type == Settings.UNDO:
            self.setObjectName("undo_button")
            self.setFixedSize(QSize(25, 25))
            self.icon = "../Resources/settings/undo"
            self.icon_size = QSize(17, 17)
            self.setToolTip("UNDO")
            self.pressed.connect(lambda: self.setting_widget.undo_canvas())

        elif self.type == Settings.REDO:
            self.setObjectName("redo_button")
            self.setFixedSize(QSize(25, 25))
            self.icon = "../Resources/settings/redo"
            self.icon_size = QSize(17, 17)
            self.setToolTip("REDO")
            self.pressed.connect(lambda: self.setting_widget.redo_canvas())

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

        # Check if the cursor is above the widget
        if event.type() == QEvent.Enter:
            self.setIcon(QIcon(f"{self.icon}_hover.png"))
            return True

        # Check if cursor left the widget
        elif event.type() == QEvent.Leave:
            self.setIcon(QIcon(f"{self.icon}.png"))
            return True

        return False


class NewCanvasDialog(QDialog):
    """
    This class will open a window dialog used to create a new canvas.
    Enter the dimensions and press ok.
    """

    def __init__(self, canvas: CanvasWidget):
        """
        Class constructor.

        :param canvas: the canvas widget to bind it to the window dialog
        """

        super(NewCanvasDialog, self).__init__()

        self.layout = QGridLayout()

        self.main_label = QLabel("Start a new drawing!")
        self.condition_label = QLabel("width  50🗙500 \nheight 50🗙250")

        self.width_label = QLabel("width")
        self.height_label = QLabel("height")

        self.canvas_width = QLineEdit()
        self.canvas_height = QLineEdit()

        self.x_label = QLabel("🗙")

        self.accept_button = QPushButton('Submit')
        self.cancel_button = QPushButton('Cancel')

        self.canvas_widget = canvas

        self.width_ok = False
        self.height_ok = False

        self.setup()

    def setup(self) -> None:
        """
        Function used to initialize the entire widget, set variables or add another widgets to it.

        :return: None
        """

        # Setup the pop-up
        self.setObjectName("new_canvas_dialog")
        self.setLayout(self.layout)
        self.setFixedSize(320, 280)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.installEventFilter(self)
        self.setStyleSheet(css(
            f"QDialog#{self.objectName()}",
            f"background-color: {BACKGROUND_DARK}",
            "border-style: solid",
            "border-width: 2px",
            f"border-color: {COLOR}",
            "border-radius: 3px"
        ))

        # Setup the layout
        self.layout.setContentsMargins(50, 50, 50, 50)
        self.layout.setSpacing(10)

        # Add the necessary widgets to the layout
        self.layout.addWidget(self.main_label, 0, 0, 1, 3, Qt.AlignCenter)
        self.layout.addWidget(self.condition_label, 1, 0, 1, 3, Qt.AlignCenter)

        self.layout.addWidget(self.width_label, 2, 0, Qt.AlignCenter)
        self.layout.addWidget(self.height_label, 2, 2, Qt.AlignCenter)

        self.layout.addWidget(self.canvas_width, 3, 0, Qt.AlignCenter)
        self.layout.addWidget(self.x_label, 3, 1, Qt.AlignCenter)
        self.layout.addWidget(self.canvas_height, 3, 2, Qt.AlignCenter)

        self.layout.addWidget(self.accept_button, 4, 0, Qt.AlignCenter)
        self.layout.addWidget(self.cancel_button, 4, 2, Qt.AlignCenter)

        # Set the check functions for the two inputs
        self.canvas_width.textEdited[str].connect(self.unlock_width)
        self.canvas_height.textEdited[str].connect(self.unlock_height)

        # Set the response functions to the buttons
        self.accept_button.clicked.connect(self.close_dialog)
        self.cancel_button.clicked.connect(self.close)

        # Set the enter button to disable to prevent bad input
        self.accept_button.setDisabled(True)

        # Set the name of the objects
        self.width_label.setObjectName("new_canvas_width_label")
        self.height_label.setObjectName("new_canvas_height_label")
        self.main_label.setObjectName("new_canvas_main_label")
        self.condition_label.setObjectName("new_canvas_condition_label")
        self.accept_button.setObjectName("new_canvas_accept")
        self.cancel_button.setObjectName("new_canvas_cancel")
        self.x_label.setObjectName("new_canvas_x_label")
        self.canvas_width.setObjectName("new_canvas_width")
        self.canvas_height.setObjectName("new_canvas_height")

        # Set the style to the width/height labels
        css_temp = css(
            f"QLabel#{self.width_label.objectName()}, QLabel#{self.height_label.objectName()}",
            "font-size: 15px",
            "font-weight: bold",
            f"color: {COLOR}"
        )
        self.width_label.setStyleSheet(css_temp)
        self.height_label.setStyleSheet(css_temp)

        # Set he style to the main label
        self.main_label.setStyleSheet(css(
            f"QLabel#{self.main_label.objectName()}",
            "font-size: 20px",
            "font-weight: bold",
            f"color: {COLOR}"
        ))

        # Set he style to the condition label
        self.condition_label.setStyleSheet(css(
            f"QLabel#{self.condition_label.objectName()}",
            "font-size: 15px",
            f"color: {COLOR}"
        ))

        # Set the style and geometry to the buttons
        self.accept_button.setFixedSize(QSize(90, 35))
        self.cancel_button.setFixedSize(QSize(90, 35))
        css_temp = merge_css(
            css(
                f"QPushButton#{self.accept_button.objectName()}, QPushButton#{self.cancel_button.objectName()}",
                "background-color: rgba(153, 170, 181, 0.1)",
                "border-style: solid",
                "border-width: 2px",
                "border-radius: 3px",
                f"border-color: {COLOR}",
                "font-size: 20px",
                f"color: {COLOR}"
            ),
            css(
                f"QPushButton#{self.accept_button.objectName()}:hover, QPushButton#{self.cancel_button.objectName()}:hover",
                "background-color: rgba(64, 78, 237, 0.1)",
                f"border-color: {COLOR_HOVER}",
                f"color: {COLOR_HOVER}",

            ),
            css(
                f"QPushButton#{self.accept_button.objectName()}:disabled",
                "background-color: rgba(139, 0, 0, 0.1)",
                f"border-color: rgb(139, 0, 0)",
                f"color: rgb(139, 0, )",

            )
        )
        self.accept_button.setStyleSheet(css_temp)
        self.cancel_button.setStyleSheet(css_temp)

        # Set the style to the X label
        self.x_label.setStyleSheet(css(
            f"QLabel#{self.x_label.objectName()}",
            "font-size: 25px",
            "font-weight: bold",
            f"color: {COLOR}"
        ))

        # Set the style and geometry to the inputs
        self.canvas_width.setFixedSize(QSize(90, 35))
        self.canvas_height.setFixedSize(QSize(90, 35))
        css_temp = merge_css(
            css(
                f"QLineEdit#{self.canvas_width.objectName()}, QLineEdit#{self.canvas_height.objectName()}",
                "background-color: rgba(153, 170, 181, 0.1)",
                "border-style: solid",
                "border-width: 2px",
                "border-radius: 3px",
                f"border-color: {COLOR}",
                "font-size: 20px",
                f"color: {COLOR}",

            ),
            css(
                f"QLineEdit#{self.canvas_width.objectName()}:focus, QLineEdit#{self.canvas_height.objectName()}:focus",
                "background-color: rgba(64, 78, 237, 0.1)",
                f"border-color: {COLOR_HOVER}",
                f"color: {COLOR_HOVER}"
            )
        )
        self.canvas_width.setStyleSheet(css_temp)
        self.canvas_height.setStyleSheet(css_temp)

    def unlock_width(self, text: str) -> None:
        """
        Functions used to check if the width is correct and enable the enter button.

        :param text: the width from input

        :return: None
        """

        # Check if the inputs are two numbers
        if text.isdecimal() and self.canvas_height.text().isdecimal():
            # Check if the input matches the limits
            if 50 <= int(text) <= 500 and 50 <= int(self.canvas_height.text()) <= 500:
                # The canvas can't be wider than a ratio of 2:1
                if int(text) >= int(self.canvas_height.text()) / 2:
                    self.accept_button.setEnabled(True)
                    return
        self.accept_button.setDisabled(True)

    def unlock_height(self, text: str) -> None:
        """
        Functions used to check if the height is correct and enable the enter button.

        :param text: the height from input

        :return: None
        """

        # Check if the inputs are two numbers
        if text.isdecimal() and self.canvas_width.text().isdecimal():
            # Check if the input matches the limits
            if 50 <= int(text) <= 500 and 50 <= int(self.canvas_width.text()) <= 500:
                # The canvas can't be wider than a ratio of 2:1
                if int(text) >= int(self.canvas_width.text()) / 2:
                    self.accept_button.setEnabled(True)
                    return
        self.accept_button.setDisabled(True)

    def close_dialog(self) -> None:
        """
        Function used to call all functions from canvas widget in order to resize and clear the canvas.
        It will also generate another grid and alpha channel with the new dimensions.
        Close the dialog window.

        :return: None
        """

        # Close the dialog window
        self.close()

        # Get the dimensions
        width = int(self.canvas_width.text())
        height = int(self.canvas_height.text())

        # If the dimensions are the same just clear the canvas to save some time
        if self.canvas_widget.canvas.canvas_width == width and self.canvas_width.canvas.canvas_height == height:
            self.canvas_widget.clear_canvas()

        # Resize the scene
        self.canvas_widget.scene.setSceneRect(0, 0, width, height)

        # Call the function from canvas widget to create again the canvas with the new dimensions
        self.canvas_widget.new_canvas(width, height)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        """
        Function used to change the css when is hovered.

        :param obj: the object
        :param event: the event
        :return: True or False if the events we wanted have occurred
        """

        # Check if the cursor is above the widget
        if event.type() == QEvent.Enter:
            self.setStyleSheet(css(
                f"QDialog#{self.objectName()}",
                f"background-color: {BACKGROUND_DARK}",
                "border-style: solid",
                "border-width: 2px",
                f"border-color: {COLOR_HOVER}",
                "border-radius: 3px"
            ))
            return True

        # Check if cursor left the widget
        elif event.type() == QEvent.Leave:
            self.setStyleSheet(css(
                f"QDialog#{self.objectName()}",
                f"background-color: {BACKGROUND_DARK}",
                "border-style: solid",
                "border-width: 2px",
                f"border-color: {COLOR}",
                "border-radius: 3px"
            ))
            return True

        return False


class ClearCanvasDialog(QDialog):
    """
    This class will open a confirm action like window dialog used to confirm the erasing of the canvas.
    Press yes or no.
    """

    def __init__(self, canvas: CanvasWidget):
        """
        Class constructor.

        :param canvas: the canvas widget to bind it to the window dialog
        """

        super(ClearCanvasDialog, self).__init__()

        self.layout = QGridLayout()

        self.yes = QPushButton('Yes')
        self.no = QPushButton('No')

        self.question = QLabel("Are you sure you want to clear the canvas?")

        self.canvas_widget = canvas

        self.setup()

    def setup(self) -> None:
        """
        Function used to initialize the entire widget, set variables or add another widgets to it.

        :return: None
        """

        # Setup the pop-up
        self.setObjectName("clear_canvas_dialog")
        self.setLayout(self.layout)
        self.setFixedSize(550, 180)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.installEventFilter(self)
        self.setStyleSheet(css(
            f"QDialog#{self.objectName()}",
            f"background-color: {BACKGROUND_DARK}",
            "border-style: solid",
            "border-width: 2px",
            f"border-color: {COLOR}",
            "border-radius: 3px"
        ))

        # Setup the layout
        self.layout.setContentsMargins(50, 50, 50, 50)
        self.layout.setSpacing(10)

        # Add the necessary widgets to the pop-up
        self.layout.addWidget(self.question, 0, 0, 1, 2, Qt.AlignCenter)

        self.layout.addWidget(self.yes, 1, 0, Qt.AlignCenter)
        self.layout.addWidget(self.no, 1, 1, Qt.AlignCenter)

        # Set the response functions to the buttons
        self.yes.clicked.connect(self.clear_canvas)
        self.no.clicked.connect(self.close)

        # Set the name of the objects
        self.question.setObjectName("clear_canvas_question")
        self.yes.setObjectName("clear_canvas_yes")
        self.no.setObjectName("clear_canvas_no")

        # Set the style to the label
        self.question.setStyleSheet(css(
            f"QLabel#{self.question.objectName()}",
            "font-size: 20px",
            "font-weight: bold",
            f"color: {COLOR}"
        ))

        # Set the style and geometry to the buttons
        self.yes.setFixedSize(QSize(90, 35))
        self.no.setFixedSize(QSize(90, 35))
        css_temp = merge_css(
            css(
                f"QPushButton#{self.yes.objectName()}, QPushButton#{self.no.objectName()}",
                "background-color: rgba(153, 170, 181, 0.1)",
                "border-style: solid",
                "border-width: 2px",
                "border-radius: 3px",
                f"border-color: {COLOR}",
                "font-size: 20px",
                f"color: {COLOR}",

            ),
            css(
                f"QPushButton#clear_canvas_yes:hover, QPushButton#clear_canvas_no:hover",
                "background-color: rgba(64, 78, 237, 0.1)",
                f"border-color: {COLOR_HOVER}",
                f"color: {COLOR_HOVER}",

            )
        )
        self.yes.setStyleSheet(css_temp)
        self.no.setStyleSheet(css_temp)

    def clear_canvas(self) -> None:
        """
        Function used to call all functions from canvas widget in order to clear the canvas.
        Close the dialog window.

        :return: None
        """

        # Close the dialog window
        self.close()

        # Call the function from canvas widget to clear the canvas
        self.canvas_widget.clear_canvas()

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        """
        Function used to change the css when is hovered.

        :param obj: the object
        :param event: the event
        :return: True or False if the events we wanted have occurred
        """

        # Check if the cursor is above the widget
        if event.type() == QEvent.Enter:
            self.setStyleSheet(css(
                f"QDialog#{self.objectName()}",
                f"background-color: {BACKGROUND_DARK}",
                "border-style: solid",
                "border-width: 2px",
                f"border-color: {COLOR_HOVER}",
                "border-radius: 3px"
            ))
            return True

        # Check if cursor left the widget
        elif event.type() == QEvent.Leave:
            self.setStyleSheet(css(
                f"QDialog#{self.objectName()}",
                f"background-color: {BACKGROUND_DARK}",
                "border-style: solid",
                "border-width: 2px",
                f"border-color: {COLOR}",
                "border-radius: 3px"
            ))
            return True

        return False
