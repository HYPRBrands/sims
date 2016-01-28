from __future__ import absolute_import

import unittest

import sims


class SimsBasicTest(unittest.TestCase):
    # just try to connect to something
    def empty_settings_test(self):
        setting = sims.get('NOT_THERE', None)
        self.assertIsNone(setting)

    def merge_to_empty_tests(self):
        expected = 1
        sims.merge({'A': expected, 'B': 2})
        actual = sims.get('A')
        self.assertEqual(actual, expected)

    def merge_on_existing_value_tests(self):
        sims.reset()

        sims.merge({'A': 1, 'B': 2})
        sims.merge({'B': 3, 'C': 4}, True)
        sims.merge({'A': 5, 'D': 6})

        self.assertEqual(sims.get('A'), 1)
        self.assertEqual(sims.get('B'), 3)
        self.assertEqual(sims.get('C'), 4)
        self.assertEqual(sims.get('D'), 6)
