from abc import abstractmethod, ABCMeta

import xlsxwriter

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

    def __init__(self, logger):
        self.logger = logger

    def write_courses(self, courses):
        """Writes the courses out"""
        for course in courses:
            students = sorted(course.students, key=lambda stu: stu.name)
            self.logger.info("Course '%s' (ID: %d) has %d participant(s): %s.", course.title, course.id, len(students), ", ".join([student.name for student in students]))

    def write_students(self, students):
        """Writes the students out"""
        for student in students:
            crse = student.course
            self.logger.info("Student '%s' assigned to course '%s' (ID: %d). Cost = %d.", student.name, crse.title, crse.id, student.cost)

class ExcelWriter(AbstractWriter):

    def __init__(self, logger):
        self.logger = logger
        # Inits the workbook
        self.workbook = xlsxwriter.Workbook('assignment.xlsx')

    def write_courses(self, courses):
        # Create a workbook and add a worksheet.
        worksheet = self.workbook.add_worksheet('Courses')
        bold = self.workbook.add_format({'bold': True})

        col = 0

        # Iterate over the data and write it out row by row.
        for course in courses:
            worksheet.write(0, col, course.title, bold)
            row = 1
            students = sorted(course.students, key=lambda stu: stu.name)
            for student in students:
                worksheet.write(row, col, student.name)
                row += 1
            col += 1


    def write_students(self, students):
        # Create a workbook and add a worksheet.
        worksheet = self.workbook.add_worksheet('Students')
        bold = self.workbook.add_format({'bold': True})

        # Header
        worksheet.write(0, 0, "Student", bold)
        worksheet.write(0, 1, "Course", bold)
        worksheet.write(0, 2, "Selection", bold)

        # Iterate over the data and write it out row by row.
        for student in students:
            row = 1
            col = 0
            crse = student.course
            worksheet.write(row, col, student.name)
            col += 1
            worksheet.write(row, col, "%s (ID: %d)" % (crse.title, crse.id))
            col += 1
            worksheet.write(row, col, student.courses)

    def close(self):
        self.workbook.close()