# -*- coding: utf-8 -*-

import logging
import unittest

import utility
from loader import CsvLoader

class UtilityTest(unittest.TestCase):

    def test_sort_students(self):
        # Get dummy logger for tests
        logger = logging.getLogger()
        logger.disabled = True
        loader = CsvLoader(logger)
        before = loader.load_students();
        names = [student.name for student in before]
        self.assertEqual(len(before), 17)
        self.assertEqual(names[0], u'Philomène')
        self.assertEqual(names[5], u'Nicolas')
        self.assertEqual(names[12], u'Lourdes')
        after = utility.sort_students(before)
        names = [student.name for student in after]
        self.assertEqual(names[0], u'Albert')
        self.assertEqual(names[5], u'Frédéric')
        self.assertEqual(names[12], u'Nicolas')

if __name__ == '__main__':
    unittest.main()