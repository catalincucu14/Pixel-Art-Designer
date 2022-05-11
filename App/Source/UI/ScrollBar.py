from PyQt5.QtWidgets import *

from Source.Utils import *


class ScrollBar(QScrollBar):
    """
    Class used to make custom scrollbar for the canvas if it is zoomed in.
    """

    def __init__(self):
        """
        Class constructor.

        """

        super(ScrollBar, self).__init__()

        self.setup()

    def setup(self) -> None:
        """
        Function used to initialize the entire widget, set variables or add another widgets to it.

        :return: None
        """

        self.setObjectName("canvas_scrollbar")

        self.setStyleSheet(merge_css(
            css(
                f"QScrollBar#{self.objectName()}:vertical",
                f"background: {BACKGROUND_DARK}",
                "border: none",
                "width: 15px",
                "margin: 0px 0px 0px 5px",
                "border-radius: 5px"
            ),
            css(
                f"QScrollBar#{self.objectName()}::handle:vertical",
                f"background-color:{COLOR}",
                "min-height: 30px",
                "border-radius: 5px"
            ),
            css(
                f"QScrollBar#{self.objectName()}::handle:vertical:hover",
                f"background-color: {COLOR_HOVER}"
            ),
            css(
                f"QScrollBar#{self.objectName()}::handle:vertical:pressed",
                f"background-color: {COLOR_HOVER}"
            ),
            css(
                f"QScrollBar#{self.objectName()}::sub-line:vertical",
                "border: none",
                f"background-color: {COLOR}",
                "background-color: transparent",
                "height: 10px",
                "height: 1px",
                "margin: 0px 0px 0px 5px",
                "border-bottom-left-radius: 5px",
                "border-bottom-right-radius: 5px",
                "border-top-left-radius: 5px",
                "border-top-right-radius: 5px",
                "subcontrol-position: top left",
                "subcontrol-origin: margin"
            ),
            css(
                f"QScrollBar#{self.objectName()}::sub-line:vertical:hover",
                f"background-color: {COLOR_HOVER}",
                "background-color: transparent"
            ),
            css(
                f"QScrollBar#{self.objectName()}::sub-line:vertical:pressed",
                f"background-color: {COLOR}",
                "background-color: transparent"
            ),
            css(
                f"QScrollBar#{self.objectName()}::add-line:vertical",
                "border: none",
                f"background-color: {COLOR}",
                "background-color: transparent",
                "height: 10px",
                "height: 1px",
                "margin: 0px 0px 0px 5px",
                "border-bottom-left-radius: 5px",
                "border-bottom-right-radius: 5px",
                "border-top-left-radius: 5px",
                "border-top-right-radius: 5px",
                "subcontrol-position: bottom",
                "subcontrol-origin: margin"
            ),
            css(
                f"QScrollBar#{self.objectName()}::add-line:vertical:hover",
                f"background-color: {COLOR_HOVER}",
                "background-color: transparent"
            ),
            css(
                f"QScrollBar#{self.objectName()}::add-line:vertical:pressed",
                f"background-color: {COLOR}",
                "background-color: transparent"
            ),
            css(
                f"QScrollBar#{self.objectName()}::up-arrow:vertical, QScrollBar#{self.objectName()}::down-arrow:vertical",
                "background: none;"
            ),
            css(
                f"QScrollBar#{self.objectName()}::add-page:vertical, QScrollBar#{self.objectName()}::sub-page:vertical",
                "background: none"
            ),
            css(
                f"QScrollBar#{self.objectName()}:horizontal",
                f"background: {BACKGROUND_DARK}",
                "border: none",
                "height: 15px",
                "margin: 5px 0px 0px 0px",
                "border-radius: 5px"
            ),
            css(
                f"QScrollBar#{self.objectName()}::handle:horizontal",
                f"background-color:{COLOR}",
                "min-width: 30px",
                "border-radius: 5px"
            ),
            css(
                f"QScrollBar#{self.objectName()}::handle:horizontal:hover",
                f"background-color: {COLOR_HOVER}"
            ),
            css(
                f"QScrollBar#{self.objectName()}::handle:horizontal:pressed",
                f"background-color: {COLOR_HOVER}"
            ),
            css(
                f"QScrollBar#{self.objectName()}::sub-line:horizontal",
                "border: none",
                f"background-color: {COLOR}",
                "background-color: transparent",
                "width: 10px",
                "width: 1px",
                "margin: 5px 0px 0px 0px",
                "border-bottom-left-radius: 5px",
                "border-bottom-right-radius: 5px",
                "border-top-left-radius: 5px",
                "border-top-right-radius: 5px",
                "subcontrol-position: top left",
                "subcontrol-origin: margin"
            ),
            css(
                f"QScrollBar#{self.objectName()}::sub-line:horizontal:hover",
                f"background-color: {COLOR_HOVER}",
                "background-color: transparent"
            ),
            css(
                f"QScrollBar#{self.objectName()}::sub-line:horizontal:pressed",
                f"background-color: {COLOR}",
                "background-color: transparent"
            ),
            css(
                f"QScrollBar#{self.objectName()}::add-line:horizontal",
                "border: none",
                f"background-color: {COLOR}",
                "background-color: transparent",
                "width: 10px",
                "width: 1px",
                "margin: 5px 0px 0px 0px",
                "border-bottom-left-radius: 5px",
                "border-bottom-right-radius: 5px",
                "border-top-left-radius: 5px",
                "border-top-right-radius: 5px",
                "subcontrol-position: top right",
                "subcontrol-origin: margin"
            ),
            css(
                f"QScrollBar#{self.objectName()}::add-line:horizontal:hover",
                f"background-color: {COLOR_HOVER}",
                "background-color: transparent"
            ),
            css(
                f"QScrollBar#{self.objectName()}::add-line:horizontal:pressed",
                f"background-color: {COLOR}",
                "background-color: transparent"
            ),
            css(
                f"QScrollBar#{self.objectName()}::up-arrow:horizontal, QScrollBar#{self.objectName()}::down-arrow:horizontal",
                "background: none;"
            ),
            css(
                f"QScrollBar#{self.objectName()}::add-page:horizontal, QScrollBar#{self.objectName()}::sub-page:horizontal",
                "background: none"
            )
        ))
