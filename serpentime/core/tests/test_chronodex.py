from unittest import TestCase
import os

from ..chronodex import Chronodex


THIS_DIR = os.path.dirname(__file__)


class TestChronodex(TestCase):

    def test_instantiation_from_txt(self):
        """Checks correct instantiation from txt file."""
        # When
        dex = Chronodex.from_txt(os.path.join(THIS_DIR, '20191113.txt'))
        expected = [
            (0, 3, 'chore', 'closet claustrophobe', 7),
            (3, 10, 'sleep', '', 5),
            (10, 11, 'food', 'cumin + coriander', 8),
            (11, 12, 'chore', 'what bus to take', 2),
            (12, 13, 'fun', 'stimuli', 8),
            (13, 15, 'work', '', 4),
            (15, 16, '', 'too calm', 6),
            (16, 17, 'seminar', 'full circle back', 8),
            (17, 18, 'seminar', 'rearview mirror', 7),
            (18, 19, 'fun', '', 10),
            (19, 20, '', 'Yoshitomo Nara', 10),
            (20, 22, '', 'distant memory', 10),
            (22, 23, 'chore', '', 9),
            (23, 24, 'work', 'ready read', 10),
        ]
        # Then
        params = [
            (act.start, act.end, act.category, act.name, act.weight)
            for act in dex.activities
        ]
        self.assertListEqual(params, expected)
