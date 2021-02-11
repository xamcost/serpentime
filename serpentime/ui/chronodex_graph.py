from PyQt5.QtWidgets import QGraphicsScene


MIN_WEDGE_ANGLE = 15 * 16
START_ANGLE = 90 * 16

WINDOW_SIZE = 600
MIN_WEDGE_SIZE_FRACTION = 1/12


class ChronodexGraph(QGraphicsScene):
    """A graphical representation of the Chronodex."""

    def __init__(self, chronodex=None):
        super().__init__()
        self.chronodex = chronodex
        self.activity_wedges = []

        self.setSceneRect(0, 0, WINDOW_SIZE, WINDOW_SIZE)
        self.center_pos = self.sceneRect().center()
        self.size = self.sceneRect().size()

        for activity in chronodex.activities:
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
        wedge: QGraphicsEllipseItem
            The Qt object representing the wedge for the given Activity.
        """
        size = activity.weight * MIN_WEDGE_SIZE_FRACTION * WINDOW_SIZE
        wedge = self.addEllipse(0, 0, size, size)
        wedge.setPos(self.center_pos - wedge.boundingRect().center())

        start, end = (activity.start, activity.end)
        wedge.setStartAngle((START_ANGLE - start * MIN_WEDGE_ANGLE))
        wedge.setSpanAngle(-MIN_WEDGE_ANGLE * (end - start))

        return wedge
