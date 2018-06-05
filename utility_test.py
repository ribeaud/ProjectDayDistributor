# -*- coding: utf-8 -*-

import logging
import random
import unittest

import utility
from loader import CsvLoader

class UtilityTest(unittest.TestCase):

    def setUp(self):
        # Get dummy logger for tests
        self.logger = logging.getLogger()
        self.logger.disabled = True
        loader = CsvLoader(self.logger)
        self.students = loader.load_students()
        self.assertEqual(len(self.students), 17)

    def test_sort_students(self):
        names = [student.name for student in self.students]
        self.assertEqual(names[0], u'Philomène')
        self.assertEqual(names[5], u'Nicolas')
        self.assertEqual(names[12], u'Lourdes')
        after = utility.sort_students(self.students)
        names = [student.name for student in after]
        self.assertEqual(names[0], u'Albert')
        self.assertEqual(names[5], u'Frédéric')
        self.assertEqual(names[12], u'Nicolas')

    def test_sort_students_with_level(self):
        levels = ['schule-5a', 'schule-5c', 'schule-10a', 'schule-9b', 'schule-7c']
        students = list(self.students)
        for student in students:
            student.level = random.choice(levels)
        after = utility.sort_students(students)
        names = [(student.name, student.level) for student in after]
        print(names)

if __name__ == '__main__':
    unittest.main()