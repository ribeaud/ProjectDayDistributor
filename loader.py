from random import shuffle

from classes import Course, Student
from parser import default_read_and_filter_csv
import pymysql.cursors

from abc import ABCMeta, abstractmethod

class AbstractLoader:
    """Abstract loader specification."""
    # meta class is used to define other classes
    __metaclass__ = ABCMeta

    @abstractmethod
    def load_courses(self):
        """Loads the courses and return them"""
        return

    @abstractmethod
    def load_students(self):
        """Loads the students and return them"""
        return

class DbLoader(AbstractLoader):
    """Loader based on database."""
    
    def __init__(self):
        # Connect to the database
        self.connection = pymysql.connect(host='localhost', user='root', password='', db='ogw', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    def load_courses(self):
        courses = []
        with self.connection.cursor() as cur:
            cur.execute("select id, title, max_students from courses")
            for row in cur:
                course = Course(int(row['id']), row['title'].strip(), int(row['max_students']))
                courses.append(course)
        return courses

    def load_students(self):
        students = []
        with self.connection.cursor() as cur:
            cur.execute("select concat(ucase(surname), ' ', givenname) as name, prioritized_list from students")
            index = 0
            for row in cur:
                students.append(Student(index, row['name'].strip(), row['prioritized_list'].strip()))
                index += 1
        return students

class CsvLoader(AbstractLoader):
    """Loader based on CSV files."""

    def load_courses(self):
        courses = []
        lines = default_read_and_filter_csv('courses.txt')
        for line in lines:
            courses.append(Course(int(line['id']), line['title'].strip(), int(line['max_students'])))
        # We sort the courses by their ID
        courses.sort(key=lambda course: course.id)
        return courses

    def load_students(self):
        students = []
        lines = default_read_and_filter_csv('students.txt')
        index = 0
        for line in lines:
            students.append(Student(index, line['name'].strip(), line['prioritized_list'].strip()))
            index += 1
        # Randomly shuffle the students
        for i in range(3):
            shuffle(students)
        return students