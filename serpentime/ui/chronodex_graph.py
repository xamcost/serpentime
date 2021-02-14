from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QColor, QBrush


MIN_WEDGE_ANGLE = 15 * 16
START_ANGLE = 90 * 16

WINDOW_SIZE = 600
MIN_WEDGE_SIZE_FRACTION = 1/12


class ChronodexGraph(QGraphicsScene):
    """A graphical representation of the Chronodex."""

    def __init__(self, chronodex, preferences):
        super().__init__()
        self._chronodex = chronodex
        self._preferences = preferences
        self.categories = self.get_categories()

        self.setSceneRect(0, 0, WINDOW_SIZE, WINDOW_SIZE)
        self.center_pos = self.sceneRect().center()
        self.size = self.sceneRect().size()

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
        self.clear()
        self.activity_wedges = []
        for activity in self._chronodex.activities:
            self.activity_wedges.append(self.add_activity_wedge(activity))

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
        """
        if activity.is_valid():
            category_prefs = self.categories.get(activity.category, {})
            if not self.preferences.get("use_custom_weight", False):
                weight = activity.weight
            else:
                weight = float(category_prefs.get('weight', activity.weight))
            size = weight * MIN_WEDGE_SIZE_FRACTION * WINDOW_SIZE
            wedge = self.addEllipse(0, 0, size, size)
            color = category_prefs.get('color', "#00FFFFFF")
            wedge.setBrush(QBrush(QColor(color)))
            wedge.setPos(self.center_pos - wedge.boundingRect().center())

            start, end = (activity.start, activity.end)
            wedge.setStartAngle((START_ANGLE - start * MIN_WEDGE_ANGLE))
            wedge.setSpanAngle(-MIN_WEDGE_ANGLE * (end - start))

            return wedge
        return None

    def get_categories(self):
        categories = {}
        for cat in self._preferences.get('categories', []):
            categories[cat['name']] = {
                key: val for key, val in cat.items() if key != 'name'
            }
        return categories
