from unittest import TestCase
import os

from ..chronodex import Chronodex


THIS_DIR = os.path.dirname(__file__)


class TestChronodex(TestCase):

    def test_instantiation_from_file(self):
        """Checks correct instantiation from txt file."""
        # When
        dex = Chronodex.from_file(os.path.join(THIS_DIR, '20191113.txt'))
        expected = [
            (0, 3, 'chore', 'closet claustrophobe'),
            (3, 10, 'sleep', ''),
            (10, 11, 'food', 'cumin + coriander'),
            (11, 12, 'chore', 'what bus to take'),
            (12, 13, 'fun', 'stimuli'),
            (13, 15, 'work', ''),
            (15, 16, '', 'too calm'),
            (16, 17, 'seminar', 'full circle back'),
            (17, 18, 'seminar', 'rearview mirror'),
            (18, 19, 'fun', ''),
            (19, 20, '', 'Yoshitomo Nara'),
            (20, 22, '', 'distant memory'),
            (22, 23, 'chore', ''),
            (23, 24, 'work', 'ready read'),
        ]
        # Then
        params = [
            (act.start_time, act.end_time, act.category, act.name)
            for act in dex.activities
        ]
        self.assertListEqual(params, expected)
