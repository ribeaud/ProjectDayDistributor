from itertools import repeat

from ortools.graph import pywrapgraph
from parser import default_read_and_filter_csv

class Course:
    '''
    A course. A course has an unique ID (a number), a title and a maximum number of students.
    For each possible student/place, we should have a numbered node. And first come first serve. It means, the cost
    should be higher for the final students.
    '''
    def __init__(self, id, title, max_students):
        self.id = id
        self.title = title
        # The number of free places left.
        self.free = self.max_students = max_students

    def __repr__(self):
        return str(self.__class__.__name__) + ": " + str(self.__dict__)

class Participant:
    def __init__(self, id, name, courses):
        self.id = id
        self.name = name
        self.courses = [int(course) for course in courses.split(',')]

    def __repr__(self):
        return str(self.__class__.__name__) + ": " + str(self.__dict__)

def load_courses():
    courses = []
    lines = default_read_and_filter_csv('courses.txt')
    node = 0
    for line in lines:
        max_students = int(line['max_students'])
        course = Course(int(line['id']), line['title'].strip(), max_students)
        to = node + max_students
        course.nodes = range(node, to)
        courses.append(course)
        node = to
    courses.sort(key=lambda course: course.id)
    return courses

def load_students():
    participants = []
    lines = default_read_and_filter_csv('students.txt')
    index = 0
    for line in lines:
        participants.append(Participant(index, line['name'], line['prioritized_list']))
        index += 1
    return participants

def create_costs(participants, courses_length):
    costs = []
    for participant in participants:
        cost = fill(courses_length, 'NA')
        # Assuming we go over all the courses this way
        for course in range(courses_length):
            if course in participant.courses:
                cost[course] = participant.courses.index(course)
        costs.append(cost)
    return costs

def fill(length, value):
    return list(repeat(value, length))

def get_course(courses, node):
    '''
    For given index returns corresponding course.
    '''
    filtered = filter(lambda course: course.id == node, courses)
    return filtered[0]

def get_student(students, index):
    return students[index]

def main():
    courses = load_courses()
    students = load_students()
    costs = create_costs(students, len(courses))
    print costs
    rows = len(costs)
    cols = len(costs[0])
    assignment = pywrapgraph.LinearSumAssignment()
    for student in range(rows):
        for course in range(cols):
            if costs[student][course] != 'NA':
                assignment.AddArcWithCost(student, course, costs[student][course])
    solve_status = assignment.Solve()
    if solve_status == assignment.OPTIMAL:
        print 'Total cost = %d' % assignment.OptimalCost()
        for i in range(0, assignment.NumNodes()):
            crse = get_course(courses, assignment.RightMate(i))
            std = get_student(students, i)
            print "Student '%s' assigned to course '%s' (%d). Cost = %d." % (std.name, crse.title, crse.id, assignment.AssignmentCost(i))
    elif solve_status == assignment.INFEASIBLE:
        print 'No assignment is possible.'
    elif solve_status == assignment.POSSIBLE_OVERFLOW:
        print 'Some input costs are too large and may cause an integer overflow.'
    print 'Finished!'

if __name__ == '__main__':
    main()
