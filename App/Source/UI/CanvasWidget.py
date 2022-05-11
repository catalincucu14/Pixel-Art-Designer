from PIL import ImageQt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Source.Tools import Tools
from Source.UI.ScrollBar import ScrollBar
from Source.UI.StatusWidget import StatusWidget
from Source.Utils import *


class CanvasWidget(QWidget):
    """
    This class will hold the canvas, the alpha channel and the grid and also to provide zooming.
    This is the main widget for canvas.
    """

    def __init__(self, status_widget: StatusWidget):
        """
        Class constructor.

        :param status_widget: the status widget to bind it to canvas in order to get the pen color and the tool used
        """

        super(CanvasWidget, self).__init__()

        self.layout = QHBoxLayout()

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)

        self.status_widget = status_widget

        self.canvas_width = 500
        self.canvas_height = 250

        self.canvas = Canvas(self.status_widget, self.canvas_width, self.canvas_height)
        self.grid = Grid(self.status_widget, self.canvas_width, self.canvas_height)
        self.alpha_channel = AlphaChannel(self.canvas_width, self.canvas_height)

        self.zoom = 0

        self.scale_to_original = 0

        self.factor = 1.1

        self.setup()

    def setup(self) -> None:
        """
        Function used to initialize the entire widget, set variables or add another widgets to it.

        :return: None
        """

        # Setup the main widget
        self.setObjectName("canvas_widget")
        self.setLayout(self.layout)
        self.layout.addWidget(self.view)

        # Setup the scene
        self.scene.addWidget(self.alpha_channel)
        self.scene.addWidget(self.canvas)
        self.scene.addWidget(self.grid)

        # Setup the view
        self.view.setObjectName("view")
        self.view.setVerticalScrollBar(ScrollBar())
        self.view.setHorizontalScrollBar(ScrollBar())

        self.view.setStyleSheet(css(
            f"QGraphicsView#{self.view.objectName()}",
            "border: 0px",
            "background-color: transparent"
        ))

        # Rescale the canvas to fit the screen
        self.rescale_canvas()

        # Add the grid to canvas
        self.canvas.grid = self.grid

    def rescale_canvas(self) -> None:
        """
        Function used to resize the canvas, zoomed in to a certain dimension.

        :return: None
        """

        # Rescale the canvas
        self.scale_to_original = 795 / self.canvas.canvas_height
        self.view.setTransform(QTransform().scale(self.scale_to_original,
                                                  self.scale_to_original))

        # Pass the canvas size to the status widget
        self.status_widget.set_position_and_zoom(zoom=self.scale_to_original)

    def clear_canvas(self) -> None:
        """
        Function used to clear the current canvas, basically creates another one.

        :return: None
        """

        self.canvas.create_canvas()

    def save_canvas(self, path: str) -> None:
        """
        Function used to save the current canvas to a given path.

        :param path: the path where the canvas will be saved
        :return: None
        """

        self.canvas.save_canvas(path)

    def new_canvas(self, width: int, height: int, image: QPixmap = None) -> None:
        """
        Function used to create a new canvas, either an empty one or from an image.

        :param width: self explanatory
        :param height: self explanatory
        :param image: self explanatory
        :return:
        """

        # Update these
        self.canvas_width = width
        self.canvas_height = height

        # Generate again the canvas with the new dimensions
        self.canvas.new_canvas(width, height, image)

        # Generate again the alpha channel with the new dimensions
        self.alpha_channel.new_alpha_channel(width, height)

        # Generate again the grid with the new dimensions
        self.grid.new_grid(width, height)

        # Rescale the new canvas
        self.rescale_canvas()

        # Reset the number of zooms to 0
        self.zoom = 0

    def undo(self) -> None:
        """
        Too hard to implement plus the lack of time ahaha.

        :return: None
        """

        self.canvas.undo()

    def redo(self) -> None:
        """
        Too hard to implement plus the lack of time ahaha.

        :return: None
        """

        self.canvas.redo()

    def wheelEvent(self, event: QWheelEvent) -> None:
        """
        Function used to zoom the canvas.

        :param event: the event
        :return: None
        """

        if event.angleDelta().y() < 0:
            # To avoid to zoom out from the initial zoom
            if self.zoom == 0:
                return

            # Increment the number of zoom ins
            self.zoom += 1

        else:

            # To avoid too many zoom ins
            if self.zoom == -11:
                return

            # Decrement the number of zoom ins
            self.zoom -= 1

        # Scale the image with the initial zoom to fit the app plus the number of additional zooms
        self.view.setTransform(QTransform().scale(self.scale_to_original * (self.factor ** (-self.zoom)),
                                                  self.scale_to_original * (self.factor ** (-self.zoom))))

        # Pass the zoom to the status widget
        self.status_widget.set_position_and_zoom(zoom=self.scale_to_original * (self.factor ** (-self.zoom)))


class Canvas(QLabel):
    """
    This class is the actual canvas that will provide draw or erase actions over an image.
    """

    def __init__(self, status_widget: StatusWidget, width=500, height=250):
        """
        Class constructor
        :param status_widget: the status widget to bind it to canvas in order to get the pen color and the tool used
        :param width: the width of the canvas as expected
        :param height: the height of the canvas as expected
        """

        super(Canvas, self).__init__()

        self.image = None

        self.canvas_width = width
        self.canvas_height = height
        self.canvas_size = QSize(self.canvas_width, self.canvas_height)

        self.status_widget = status_widget

        self.pen_color = QColor("#010000")
        self.pen_size = 1

        self.grid = None

        self.tool = Tools.PEN

        self.drawing = True

        self.current_point = None
        self.last_point = None

        self.setup()

    def setup(self) -> None:
        """
        Function used to initialize the entire widget, set variables or add another widgets to it.

        :return: None
        """

        # Setup the canvas
        self.setObjectName("canvas")
        self.setFixedSize(self.canvas_size)
        self.create_canvas()
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(css(
            "QLabel#canvas",
            "background-color: transparent"
        ))

        # Pass the canvas size to the status widget
        self.status_widget.set_dimensions_and_tool(width=self.canvas_width, height=self.canvas_height)

    def new_canvas(self, width: int, height: int, image: QPixmap = None) -> None:
        """
        Function used to create a new canvas, either an empty one or from an image.

        :param width: self explanatory
        :param height: self explanatory
        :param image: self explanatory
        :return: None
        """

        # Change the size of the canvas
        self.canvas_width = width
        self.canvas_height = height
        self.canvas_size = QSize(self.canvas_width, self.canvas_height)

        # Resize the canvas
        self.setFixedSize(self.canvas_size)

        # Create again the canvas with an image or a clear one
        if image is not None:
            self.setPixmap(image)
        else:
            # Create the new canvas
            self.create_canvas()

        # Give the dimensions to the status widget
        self.status_widget.set_dimensions_and_tool(width=self.canvas_width, height=self.canvas_height)

    def save_canvas(self, path: str) -> None:
        """
        Function used to save the current canvas to a given path.

        :param path: the path where the canvas will be saved
        :return: None
        """

        # Save the image to the chosen path
        self.image = ImageQt.fromqpixmap(self.pixmap())
        self.image.save(path)

    def create_canvas(self) -> None:
        """
        Function used to create an empty canvas.

        :return: None
        """

        # Create a transparent pixmap
        pixmap = QPixmap(self.canvas_width, self.canvas_height)
        pixmap.fill(QColor(0, 0, 0, 0))

        # Set the pixmap to canvas
        self.setPixmap(pixmap)

    def set_tool(self, tool: Tools) -> None:
        """
        Function used to change the current tool, called from tools.

        :param tool: the tool to be changed
        :return: None
        """

        self.tool = tool

        # Pass the canvas tool to the status widget
        self.status_widget.set_dimensions_and_tool(tool=tool)

    def get_tool(self) -> Tools:
        """
        Function used to get the current tool. Useless more or less.

        :return: the current tool
        """

        return self.tool

    def set_pen_color(self, color: str) -> None:
        """
        Function used to change the color used to draw.

        :param color: the hexadecimal value of the color
        :return:
        """

        self.pen_color = QColor(color)

        # Pass the canvas pen color to the status widget
        self.status_widget.set_color(color)

        # Change to pen if we change the color
        if self.tool == Tools.ERASER:
            self.set_tool(Tools.PEN)

        # Pass the canvas tool to the status widget
        self.status_widget.set_dimensions_and_tool(tool=self.tool)

    def set_pen_size(self, value: str) -> None:
        """
        Function used to change the size of the pen.
        Is used to change the thickness of the circle, square and brush as well.

        :param value: the size
        :return: None
        """

        self.pen_size = int(value)

    def undo(self) -> None:
        """
        Too hard to implement plus the lack of time ahaha.

        :return: None
        """

        # TODO
        pass

    def redo(self) -> None:
        """
        Too hard to implement plus the lack of time ahaha.

        :return: None
        """

        # TODO
        pass

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """
        Function used to handle the event when the mouse is released after being pressed.

        :param event: the event
        :return: None
        """

        # Check if left click was released
        if event.button() == Qt.LeftButton:
            self.drawing = False

        # A dummy switch to call the function based on the selected tool
        tools = {
            Tools.LINE: self.draw_line,
            Tools.SQUARE: self.draw_square,
            Tools.CIRCLE: self.draw_circle,
            Tools.BRUSH: self.brush
        }
        try:
            tools.get(self.tool)(event)
        except:
            pass

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        Function used to handle the event when the mouse is pressed.

        :param event: the event
        :return: None
        """

        # Check if left click is pressed
        if event.button() == Qt.LeftButton:
            self.drawing = True

            # Clear de grid because will look bad when starting to draw because the grid point will remain there
            self.grid.clear_grid()

            # Set the position of the cursor when was pressed
            self.last_point = event.pos()

        # A dummy switch to call the function based on the selected tool
        tools = {
            Tools.PEN: self.draw_point,
            Tools.ERASER: self.erase_points,
            Tools.LINE: self.draw_line,
            Tools.SQUARE: self.draw_square,
            Tools.CIRCLE: self.draw_circle,
            Tools.BRUSH: self.brush,
            Tools.FILL: self.fill,
            Tools.PICKER: self.pick_color
        }
        try:
            tools.get(self.tool)(event)
        except:
            pass

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """
        Function used to handle the event when the mouse is moved.

        :param event: the event
        :return: None
        """

        # A dummy switch to call the function based on the selected tool
        tools = {
            Tools.PEN: self.draw_points,
            Tools.ERASER: self.erase_points,
            Tools.LINE: self.update_current_point,
            Tools.SQUARE: self.update_current_point,
            Tools.CIRCLE: self.update_current_point,
            Tools.BRUSH: self.brush
        }
        try:
            tools.get(self.tool)(event)
        except:
            pass

    def paintEvent(self, event: QPaintEvent) -> None:
        """
        Function used to update the canvas when a paint event occurs.

        :param event: the event
        :return: None
        """

        painter = QPainter(self)

        painter.setPen(QPen(self.pen_color,
                            self.pen_size,
                            Qt.SolidLine,
                            Qt.SquareCap,
                            Qt.RoundJoin))

        painter.drawPixmap(self.rect(), self.pixmap())

        if self.last_point and self.current_point:
            # Draw a temporary line over Canvas
            if self.tool == Tools.LINE:
                painter.drawLine(self.last_point, self.current_point)

            # Draw a temporary square over Canvas
            if self.tool == Tools.SQUARE:
                painter.drawLine(self.last_point, QPoint(self.last_point.x(), self.current_point.y()))
                painter.drawLine(self.last_point, QPoint(self.current_point.x(), self.last_point.y()))
                painter.drawLine(QPoint(self.last_point.x(), self.current_point.y()), self.current_point)
                painter.drawLine(QPoint(self.current_point.x(), self.last_point.y()), self.current_point)

            # Draw a temporary ellipse over Canvas
            if self.tool == Tools.CIRCLE:
                painter.drawEllipse(self.last_point,
                                    self.current_point.x() - self.last_point.x(),
                                    self.current_point.y() - self.last_point.y())

    def draw_point(self, event: QMouseEvent) -> None:
        """
        Function used to draw a point.

        :param event: the event
        :return: None
        """

        if self.drawing:
            painter = QPainter(self.pixmap())

            painter.setPen(QPen(self.pen_color,
                                self.pen_size,
                                Qt.SolidLine,
                                Qt.SquareCap,
                                Qt.RoundJoin))

            painter.drawPoint(event.pos())

            painter.end()

            self.update()

            self.last_point = event.pos()

    def draw_points(self, event: QMouseEvent) -> None:
        """
        Function used to draw points after the cursor.

        :param event: the event
        :return: None
        """

        if self.drawing:
            painter = QPainter(self.pixmap())

            painter.setPen(QPen(self.pen_color,
                                self.pen_size,
                                Qt.SolidLine,
                                Qt.RoundCap,
                                Qt.RoundJoin))

            painter.drawLine(self.last_point, event.pos())

            painter.end()

            self.update()

            self.last_point = event.pos()

    def erase_points(self, event: QMouseEvent) -> None:
        """
        Function used to erase points after the cursor.

        :param event: the event
        :return: None
        """

        if self.drawing:
            painter = QPainter(self.pixmap())

            painter.setPen(QPen(self.pen_color,
                                self.pen_size,
                                Qt.SolidLine,
                                Qt.RoundCap,
                                Qt.RoundJoin))

            painter.save()

            r = QRect(QPoint(), self.pen_size * QSize())
            r.moveCenter(event.pos())

            painter.setCompositionMode(QPainter.CompositionMode_Clear)

            painter.eraseRect(r)

            painter.end()

            self.update()

            self.last_point = event.pos()

    def draw_line(self, event: QMouseEvent) -> None:
        """
        Function used to draw a line between 2 points.

        :param event: the event
        :return: None
        """

        painter = QPainter(self.pixmap())

        painter.setPen(QPen(self.pen_color,
                            self.pen_size,
                            Qt.SolidLine,
                            Qt.SquareCap,
                            Qt.RoundJoin))

        painter.drawLine(self.last_point, self.current_point)

        painter.end()

        self.update()

        self.last_point = self.current_point = None

    def draw_square(self, event: QMouseEvent) -> None:
        """
        Function used to draw a square.

        :param event: the event
        :return: None
        """

        painter = QPainter(self.pixmap())

        painter.setPen(QPen(self.pen_color,
                            self.pen_size,
                            Qt.SolidLine,
                            Qt.SquareCap,
                            Qt.RoundJoin))

        painter.drawLine(self.last_point, QPoint(self.last_point.x(), event.pos().y()))
        painter.drawLine(self.last_point, QPoint(event.pos().x(), self.last_point.y()))
        painter.drawLine(QPoint(self.last_point.x(), event.pos().y()), event.pos())
        painter.drawLine(QPoint(event.pos().x(), self.last_point.y()), event.pos())

        painter.end()

        self.update()

        self.last_point = event.pos()
        self.current_point = None

    def draw_circle(self, event: QMouseEvent) -> None:
        """
        Function used to draw a circle.

        :param event: the event
        :return: None
        """

        painter = QPainter(self.pixmap())

        painter.setPen(QPen(self.pen_color,
                            self.pen_size,
                            Qt.SolidLine,
                            Qt.RoundCap,
                            Qt.RoundJoin))

        painter.drawEllipse(self.last_point,
                            self.current_point.x() - self.last_point.x(),
                            self.current_point.y() - self.last_point.y())
        painter.end()

        self.update()

        self.last_point = self.current_point = None

    def brush(self, event: QMouseEvent) -> None:
        """
        Function used to draw points after the cursor with a brush effect.

        :param event: the event
        :return: None
        """

        if self.drawing:
            painter = QPainter(self.pixmap())

            painter.setPen(QPen(self.pen_color,
                                self.pen_size,
                                Qt.SolidLine,
                                Qt.RoundCap,
                                Qt.RoundJoin))

            painter.setOpacity(0.15)

            for i in range(2):
                for j in range(2):
                    painter.drawLine(QPoint(self.last_point.x() + i, self.last_point.y() + j),
                                     QPoint(event.pos().x() + i, event.pos().y() + j))
                    painter.drawLine(QPoint(self.last_point.x() + i, self.last_point.y() - j),
                                     QPoint(event.pos().x() + i, event.pos().y() - j))
                    painter.drawLine(QPoint(self.last_point.x() - i, self.last_point.y() + j),
                                     QPoint(event.pos().x() - i, event.pos().y() + j))
                    painter.drawLine(QPoint(self.last_point.x() - i, self.last_point.y() - j),
                                     QPoint(event.pos().x() - i, event.pos().y() - j))

            painter.setOpacity(1.0)

            painter.drawLine(self.last_point, event.pos())

            painter.end()

            self.update()

            self.last_point = event.pos()

    def fill(self, event: QMouseEvent) -> None:
        """
        Function used to replace a color with another color from a section.

        :param event: the event
        :return: None
        """

        painter = QPainter(self.pixmap())

        painter.setPen(QPen(self.pen_color,
                            1,
                            Qt.SolidLine,
                            Qt.RoundCap,
                            Qt.RoundJoin))

        image = self.pixmap().toImage()

        # Extract the color of the target pixel, if is on the png part of the image it will be black
        color = QColor(image.pixel(event.pos()))

        # Draw the first point, where was pressed
        painter.drawPoint(self.last_point)

        self.recursive_fill(self.last_point.x(), self.last_point.y(), color, painter)

        painter.end()

        self.update()

        self.last_point = event.pos()

        # Switch immediately to the pen because why not
        self.set_tool(Tools.PEN)

    def recursive_fill(self, x: int, y: int, color: QColor, painter: QPainter) -> None:
        """
        Function used to do the actual fill.

        :param x: self explanatory
        :param y: self explanatory
        :param color: self explanatory
        :param painter: the painter use to draw
        :return: None
        """

        image = self.pixmap().toImage()

        if QColor(image.pixel(x + 1, y)) == color:
            painter.drawPoint(QPoint(x + 1, y))
            self.update()
            self.recursive_fill(x + 1, y, color, painter)

        if QColor(image.pixel(x, y + 1)) == color:
            painter.drawPoint(QPoint(x, y + 1))
            self.update()
            self.recursive_fill(x, y + 1, color, painter)

        if QColor(image.pixel(x - 1, y)) == color:
            painter.drawPoint(QPoint(x - 1, y))
            self.update()
            self.recursive_fill(x - 1, y, color, painter)

        if QColor(image.pixel(x, y - 1)) == color:
            painter.drawPoint(QPoint(x, y - 1))
            self.update()
            self.recursive_fill(x, y - 1, color, painter)

    def pick_color(self, event: QMouseEvent) -> None:
        """
        Function used to pick a color from a certain pixel.

        :param event: the event
        :return: None
        """

        # Convert the pixmap into a image
        image = self.pixmap().toImage()

        # Extract the color of the target pixel, if is on the png part of the image it will be black
        color = QColor(image.pixel(event.pos()))

        # Update the position because it will do weird stuff if not
        self.last_point = event.pos()

        # Set the color to the pen
        self.set_pen_color(color.name())

        # Switch immediately to the pen because why not
        self.set_tool(Tools.PEN)

    def update_current_point(self, event: QMouseEvent) -> None:
        """
        Function used to change a variable.

        :param event: the event
        :return: None
        """

        if self.last_point:
            self.current_point = event.pos()
            self.update()


class AlphaChannel(QLabel):
    """
    This class will provide those white and gray dots seen in every similar project.
    I makes drawing easier and it looks cool.
    """

    def __init__(self, width=500, height=250):
        """
        Class constructor.

        :param width: the width of the canvas as expected
        :param height: the height of the canvas as expected
        """

        super(AlphaChannel, self).__init__()

        self.canvas_width = width
        self.canvas_height = height
        self.canvas_size = QSize(width, height)

        self.image = None

        self.setup()

    def setup(self) -> None:
        """
        Function used to initialize the entire widget, set variables or add another widgets to it.

        :return: None
        """

        # Setup the alpha channel
        self.setObjectName("alpha_channel")
        self.setFixedSize(self.canvas_size)
        self.setAlignment(Qt.AlignCenter)
        self.create_alpha_channel()
        self.setStyleSheet(css(
            "QLabel#alpha_channel",
            "background-color: transparent"
        ))

    def create_alpha_channel(self) -> None:
        """
        Function used to create a new alpha channel with dimensions of the canvas.

        :return: None
        """

        # Create a white image and paint 1 of 2 pixels in gray
        self.image = QImage(self.canvas_size, QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.setPixmap(QPixmap(self.image))

        painter = QPainter(self.pixmap())

        painter.setPen(QPen(QColor("#d9d9d9"),
                            1,
                            Qt.SolidLine,
                            Qt.RoundCap,
                            Qt.RoundJoin))

        for i in range(self.canvas_width):
            for j in range(self.canvas_height):
                if (i % 2 == 1 and j % 2 == 1) or (i % 2 == 0 and j % 2 == 0):
                    painter.drawPoint(QPoint(i, j))

        painter.end()

        self.update()

    def new_alpha_channel(self, width: int, height: int) -> None:
        """
        Function used to create a new alpha channel with dimensions of the canvas.

        :return: None
        """

        # Change the size of the alpha channel
        self.canvas_width = width
        self.canvas_height = height
        self.canvas_size = QSize(self.canvas_width, self.canvas_height)
        self.setFixedSize(self.canvas_size)

        # Create again the alpha channel
        self.create_alpha_channel()


class Grid(QLabel):
    """
    This class will indicate on which pixel is the cursor and look cool and professional.
    """

    def __init__(self, status_widget: StatusWidget, width=500, height=250):
        """

        :param status_widget: the status widget to bind it to canvas in order to get the pen color and the tool used
        :param width: the width of the canvas as expected
        :param height: the height of the canvas as expected
        """

        super(Grid, self).__init__()

        self.status_widget = status_widget

        self.image = None

        self.canvas_width = width
        self.canvas_height = height
        self.canvas_size = QSize(width, height)

        self.last_point = None

        self.color = QColor(0, 0, 0, 75)

        self.setup()

    def setup(self) -> None:
        """
        Function used to initialize the entire widget, set variables or add another widgets to it.

        :return: None
        """

        # Setup the grid
        self.setObjectName("grid")
        self.setFixedSize(self.canvas_size)
        self.setAlignment(Qt.AlignCenter)
        self.create_clear_grid()
        self.setMouseTracking(True)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(css(
            "QLabel#grid",
            "background-color: transparent"
        ))

    def new_grid(self, width: int, height: int) -> None:
        """
        Function used to create a new grid.

        :param width: self explanatory
        :param height: self explanatory
        :return: None
        """

        # Change the size of the grid
        self.canvas_width = width
        self.canvas_height = height
        self.canvas_size = QSize(self.canvas_width, self.canvas_height)
        self.setFixedSize(self.canvas_size)

        # Create the new alpha grid
        self.create_clear_grid()

    def create_clear_grid(self) -> None:
        """
        Function used to create a new grid.

        :return:
        """

        # Create a transparent pixmap
        pixmap = QPixmap(self.canvas_size)
        pixmap.fill(QColor(0, 0, 0, 0))

        self.setPixmap(pixmap)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """
        Function used to handle the event when the mouse is moved.

        :param event: the event
        :return: None
        """

        painter = QPainter(self.pixmap())

        painter.setPen(QPen(self.color,
                            1,
                            Qt.SolidLine,
                            Qt.RoundCap,
                            Qt.RoundJoin))

        self.clear_grid(painter)

        painter.drawPoint(event.pos())

        painter.end()

        self.update()

        self.last_point = event.pos()

        # Pass the cursor position to the status widget
        self.status_widget.set_position_and_zoom(x=event.x(), y=event.y())

    def clear_grid(self, painter: QPainter = None) -> None:
        """
        Function hard to explain.

        :param painter: the event
        :return: None
        """
        if painter is None:
            painter = QPainter(self.pixmap())

            painter.setPen(QPen(self.color,
                                1,
                                Qt.SolidLine,
                                Qt.RoundCap,
                                Qt.RoundJoin))

        # Check if is a point painted on grid, if true delete it
        if self.last_point is not None:
            painter.save()

            r = QRect(QPoint(), 1 * QSize())
            r.moveCenter(QPoint(self.last_point))

            painter.setCompositionMode(QPainter.CompositionMode_Clear)

            painter.eraseRect(r)

            painter.restore()

        if painter is None:
            painter.end()

            self.update()
