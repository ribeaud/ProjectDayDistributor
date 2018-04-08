from abc import abstractmethod, ABCMeta

import xlsxwriter

from classes import Course


class AbstractWriter:
    """Abstract writer specification."""
    # meta class is used to define other classes
    __metaclass__ = ABCMeta

    @abstractmethod
    def write_courses(self, courses):
        """Writes the courses out"""
        return

    @abstractmethod
    def write_students(self, students):
        """Writes the students out"""
        return

    def close(self):
        return

class ConsoleWriter(AbstractWriter):

    def write_courses(self, courses):
        """Writes the courses out"""
        for course in courses:
            students = sorted(course.students, key=lambda stu: stu.name)
            print "Course '%s' (ID: %d) has %d participant(s): %s" % (course.title, course.id, len(students), ", ".join([student.name for student in students]))

    def write_students(self, students):
        """Writes the students out"""
        for student in students:
            crse = student.course
            print "Student '%s' assigned to course '%s' (ID: %d). Cost = %d." % (student.name, crse.title, crse.id, student.cost)

class ExcelWriter(AbstractWriter):

    def __init__(self):
        # Inits the workbook
        self.workbook = xlsxwriter.Workbook('assignment.xlsx')

    def write_courses(self, courses):
        # Create a workbook and add a worksheet.
        worksheet = self.workbook.add_worksheet('Courses')
        bold = self.workbook.add_format({'bold': True})

        col = 0

        # Iterate over the data and write it out row by row.
        for course in courses:
            row = 0
            worksheet.write(row, col, course.title, bold)
            row += 1
            students = sorted(course.students, key=lambda stu: stu.name)
            for student in students:
                worksheet.write(row, col, student.name)
                row += 1
            col += 1


    def write_students(self, students):
        pass

    def close(self):
        self.workbook.close()