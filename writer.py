from abc import abstractmethod, ABCMeta

import xlsxwriter

import utility


def get_course_by_id(courses, id):
    '''
    For given ID returns corresponding course.
    '''
    filtered = filter(lambda course: course.id == id, courses)
    return filtered[0]

def student_name(student):
    '''
    Outputs student name appended by his level if present
    '''
    if (hasattr(student, 'level')):
        return "%s (%s)" % (student.name, student.level)
    else:
        return student.name

class AbstractWriter:
    """Abstract writer specification."""
    # meta class is used to define other classes
    __metaclass__ = ABCMeta

    @abstractmethod
    def write_courses(self, courses):
        """Writes the courses out"""
        return

    @abstractmethod
    def write_students(self, students, courses):
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
            students = utility.sort_students(course.students)
            self.logger.info("Course '%s' (ID: %d) has %d participant(s): %s.", course.title, course.id, len(students), ", ".join([student_name(student) for student in students]))

    def write_students(self, students, courses):
        """Writes the students out"""
        for student in students:
            course = get_course_by_id(courses, student.course)
            selection = ["'" + get_course_by_id(courses, course_id).title + "'" for course_id in student.courses]
            self.logger.info("Student '%s' assigned to course '%s' (ID: %d). Selection = [%s]. Cost = %d.", student_name(student), course.title, course.id, ', '.join(selection), student.cost)

class ExcelWriter(AbstractWriter):

    def __init__(self, logger):
        self.logger = logger
        # Inits the workbook
        self.workbook = xlsxwriter.Workbook('assignment.xlsx')

    def write_courses(self, courses):
        # Add 'Courses' worksheet.
        worksheet = self.workbook.add_worksheet('Courses')
        bold = self.workbook.add_format({'bold': True})

        col = 0

        # Iterate over the data and write them out row by row.
        for course in courses:
            worksheet.write(0, col, course.title + (" (ID: %d)" % course.id), bold)
            worksheet.write(1, col, "Max: %d" % course.max_students, bold)
            row = 3
            students = utility.sort_students(course.students)
            for student in students:
                worksheet.write(row, col, student_name(student))
                row += 1
            col += 1


    def write_students(self, students, courses):
        # Add 'Students' worksheet.
        worksheet = self.workbook.add_worksheet('Students')
        bold = self.workbook.add_format({'bold': True})

        # Header
        worksheet.write(0, 0, "Student", bold)
        worksheet.write(0, 1, "Course", bold)
        worksheet.write(0, 2, "Selection", bold)

        row = 1

        # Iterate over the students.
        for student in students:
            col = 0
            course = get_course_by_id(courses, student.course)
            selection = [get_course_by_id(courses, course_id).title for course_id in student.courses]
            worksheet.write(row, col, student_name(student))
            col += 1
            worksheet.write(row, col, "%s (ID: %d)" % (course.title, course.id))
            col += 1
            worksheet.write(row, col, ', '.join(selection))
            row += 1

    def close(self):
        self.workbook.close()