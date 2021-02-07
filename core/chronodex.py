class Activity(object):
    """A class representing an activity during a day."""

    def __init__(self, start_time, end_time=None, name='', category=''):
        self.start_time = start_time
        self.end_time = end_time
        self.name = name
        self.category = category


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
                        activities.append(
                            Activity(
                                start_time=int(params[0]),
                                end_time=None,
                                category=params[1],
                                name=params[3],
                            )
                        )
        # Fills the end time of the activities
        if len(activities) > 1:
            for ind, activity in enumerate(activities[1:]):
                activities[ind].end_time = activity.start_time
        activities[-1].end_time = 24

        return cls(activities)
