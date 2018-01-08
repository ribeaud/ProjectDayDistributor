from random import shuffle

from classes import Course, Student
from parser import default_read_and_filter_csv

def load_courses():
    courses = []
    lines = default_read_and_filter_csv('courses.txt')
    for line in lines:
        max_students = int(line['max_students'])
        course = Course(int(line['id']), line['title'].strip(), max_students)
        courses.append(course)
    # We sort the courses by their ID
    courses.sort(key=lambda course: course.id)
    return courses

def load_students():
    students = []
    lines = default_read_and_filter_csv('students.txt')
    index = 0
    for line in lines:
        students.append(Student(index, line['name'], line['prioritized_list']))
        index += 1
    # Randomly shuffle the students
    shuffle(students)
    return students

