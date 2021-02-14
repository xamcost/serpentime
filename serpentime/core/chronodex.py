class Activity(object):
    """A class representing an activity during a day."""

    def __init__(self, start=None, end=None, name='', category='', weight=5):
        self.start = start
        self.end = end
        self.name = name
        self.category = category
        self.weight = weight

    def is_valid(self):
        if not isinstance(self.start, (int, float)):
            return False
        if not isinstance(self.end, (int, float)):
            return False
        checks = [
            self.start >= 0, self.start < 24,
            self.end >= 0, self.end < 24,
            self.weight >= 0, self.weight <= 10,
        ]
        return all(checks)


class Chronodex(object):
    """Represents a list of activities for one day."""

    def __init__(self, activities=None):
        self.activities = activities or []

    @classmethod
    def from_file(cls, path):
        """Returns a Chronodex instance from a txt file.
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
