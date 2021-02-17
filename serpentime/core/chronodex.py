class Activity(object):
    """A class representing an activity during a day."""

    def __init__(self, start=None, end=None, name='', category='', weight=5):
        """Initialises one activity of the day.

        Parameters
        ----------
        start: float or None
            The starting time of the activity. It should be a float between
            0 and 24. If None, the activity is not valid, and will therefore
            not be represented in a chronodex graph.
        end: float or None
            The ending time of the activity. It should be a float between
            0 and 24. If None, the activity is not valid, and will therefore
            not be represented in a chronodex graph.
        name: str
            Name of the activity.
        category: str
            The category this activity belongs to (< work > or < chore > for
            instance).
        weight: float
            A weight for the graphical representation of this activity.
            It should be between 0 and 10, otherwise the activity is invalid.
        """
        self.start = start
        self.end = end
        self.name = name
        self.category = category
        self.weight = weight

    def is_valid(self):
        """Whether or not this activity has valid attribute values.
        """
        if not isinstance(self.start, (int, float)):
            return False
        if not isinstance(self.end, (int, float)):
            return False
        checks = [
            self.start >= 0, self.start <= 24,
            self.end >= 0, self.end <= 24,
            self.weight >= 0, self.weight <= 10,
        ]
        return all(checks)


class Chronodex(object):
    """Represents a list of activities for one day."""

    def __init__(self, activities=None):
        """Represents a list of activities for one day.

        Parameters
        ----------
        activities: list(serpentime.core.Activity)
            The list of activity composing this Chronodex.
        """
        self.activities = activities or []

    @classmethod
    def from_txt(cls, path):
        """Returns a Chronodex instance from a txt file.

        Txt files are handled mostly to ensure old chronodex can be loaded.
        Their rows are structured in the following way:
        start, category, weight, name

        Parameters
        ----------
        path: str
            The full filename to use to create the Chronodex instance.

        Returns
        -------
        The Chronodex instance corresponding to the given path.
        """
        activities = []
        with open(path, 'r') as fid:
            for line in fid:
                params = [elt.strip() for elt in line.split(',')]
                if any([param != '' for param in params[1:]]):
                    if params[0].isnumeric():
                        weight = params[2]
                        if weight.isnumeric():
                            weight = int(weight)
                        else:
                            weight = 10
                        activities.append(
                            Activity(
                                start=int(params[0]),
                                end=None,
                                category=params[1],
                                name=params[3],
                                weight=weight,
                            )
                        )
        # Fills the end time of the activities
        if len(activities) > 1:
            for ind, activity in enumerate(activities[1:]):
                activities[ind].end = activity.start
        activities[-1].end = 24

        return cls(activities)

    @classmethod
    def from_csv(cls, path):
        """Returns a Chronodex instance from a csv file.

        Csv files differs from txt files by their structure, holding also
        the end time of the activities:
        start, end, category, name, weight

        Parameters
        ----------
        path: str
            The full filename to use to create the Chronodex instance.

        Returns
        -------
        The Chronodex instance corresponding to the given path.
        """
        activities = []
        with open(path, 'r') as fid:
            for line in fid:
                params = [elt.strip() for elt in line.split(',')]
                if len(params) == 5:
                    activities.append(
                        Activity(
                            start=float(params[0]),
                            end=float(params[1]),
                            category=params[2],
                            name=params[3],
                            weight=float(params[4]),
                        )
                    )

        return cls(activities)
