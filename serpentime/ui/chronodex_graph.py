from math import cos, pi, sin

from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QBrush, QColor, QFont, QPen


# Conversion factor for angle, from degree to radian
TO_RAD = pi / 180
# Wedge angle in Qt are in 1/16 of degree
QT_ANGLE_FRACTION = 16
# The minimal angle of a wedge: corresponds to 1h in a day, so 360/24 = 15
MIN_WEDGE_ANGLE = 15 * QT_ANGLE_FRACTION
# Midnight is at 90 degree
START_ANGLE = 90 * QT_ANGLE_FRACTION

# The desired window size
WINDOW_SIZE = 600
# The minimal radius of an activity wedge, as a fraction of window size
MIN_WEDGE_SIZE_FRACTION = 1/12


class ChronodexGraph(QGraphicsScene):
    """A graphical representation of the Chronodex."""

    def __init__(self, chronodex, preferences):
        """Handles the chronodex graphical design.

        Parameters
        ----------
        chronodex: serpentime.core.Chronodex
            The Chronodex instance to be rendered.
        preferences: dict
            A dictionary holding the settings for the chronodex graphical
            representation (color and weight for the activities, etc...).
        """
        super().__init__()
        self._chronodex = chronodex
        self._preferences = preferences
        self.categories = self.get_categories()

        self.setSceneRect(0, 0, WINDOW_SIZE, WINDOW_SIZE)
        self.center_pos = self.sceneRect().center()

        self.draw_chronodex()

    @property
    def chronodex(self):
        return self._chronodex

    @chronodex.setter
    def chronodex(self, value):
        self._chronodex = value
        self.draw_chronodex()

    @property
    def preferences(self):
        return self._preferences

    @preferences.setter
    def preferences(self, value):
        self._preferences = value
        self.categories = self.get_categories()
        self.draw_chronodex()

    def draw_chronodex(self):
        """Redraws the chronodex graph.
        """
        self.clear()

        if self.preferences.get("show_overlay", False):
            for frac in [2, 4, 6, 8, 10]:
                size = frac * MIN_WEDGE_SIZE_FRACTION * WINDOW_SIZE
                x, y = (self.center_pos.x(), self.center_pos.y())
                circ = self.addEllipse(x, y, size, size)
                circ.setPos(self.center_pos - circ.boundingRect().center())
                circ.setPen(QPen(QColor("grey")))

        self.activity_wedges = []
        self.activity_labels = []
        for activity in self._chronodex.activities:
            wedge, label = self.add_activity_wedge(activity)
            self.activity_wedges.append(wedge)
            self.activity_labels.append(label)

    def add_activity_wedge(self, activity):
        """Draws and returns the wedge corresponding to the given
        Activity instance.

        Parameters
        ----------
        activity: serpentime.core.Activity
            The activity to be sketched in the Chronodex.

        Returns
        -------
        wedge: QGraphicsEllipseItem or None
            The Qt object representing the wedge for the given Activity.
            If Activity.is_valid() is False, returns None.
        text: QGraphicsTextItem or None
            The Qt object representing the activity name. None if the
            activity is not valid
        """
        wedge = None
        text = None
        if activity.is_valid():
            category_prefs = self.categories.get(activity.category, {})
            if self.preferences.get("use_custom_weight", False):
                weight = activity.weight
            else:
                weight = float(category_prefs.get('weight', activity.weight))
            size = weight * MIN_WEDGE_SIZE_FRACTION * WINDOW_SIZE
            wedge = self.addEllipse(0, 0, size, size)
            color = category_prefs.get('color', "#FFFFFF")
            wedge.setBrush(QBrush(QColor(color)))
            wedge.setPos(self.center_pos - wedge.boundingRect().center())

            start, end = (activity.start, activity.end)
            start_angle = START_ANGLE - start * MIN_WEDGE_ANGLE
            span_angle = -MIN_WEDGE_ANGLE * (end - start)
            wedge.setStartAngle(start_angle)
            wedge.setSpanAngle(span_angle)

            text = None
            if self.preferences.get("show_labels", False):
                txt_angle = (start_angle + 0.5 * span_angle)
                txt_angle /= QT_ANGLE_FRACTION
                txt_angle *= TO_RAD
                x_txt = 0.5 * size * cos(txt_angle)
                y_txt = 0.5 * size * sin(txt_angle)
                text = self.addText(activity.name)
                text.setPos(self.center_pos - text.boundingRect().center())
                text.moveBy(x_txt, -y_txt)
                # Rotates the label
                if self.preferences.get("rotate_labels", False):
                    text.setTransformOriginPoint(text.boundingRect().center())
                    rot_angle = - txt_angle * 180 / pi
                    if activity.start >= 12:
                        rot_angle += 180
                    text.setRotation(rot_angle)
                # Brings the label to front, on top of wedges
                text.setZValue(1)
                # Sets text bold and grey
                font = QFont()
                font.setBold(True)
                text.setFont(font)
                text.setDefaultTextColor(QColor("grey"))

        return wedge, text

    def get_categories(self):
        """Returns a dictionary mapping activities' categories' names to
        a dictionary containing the settings for these categories, based
        on the preferences stored in :attr:`preferences`.

        Returns
        -------
        categories: dict
            A dictionary of type
            {category_name: {'color': '#FFFFFF', 'weight': 5, 'aliases': []}}.
        """
        categories = {}
        for cat in self._preferences.get('categories', []):
            categories[cat['name']] = {
                key: val for key, val in cat.items() if key != 'name'
            }
        return categories
