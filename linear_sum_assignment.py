import sys
from ortools.graph import pywrapgraph

from loader import load_courses, load_students
from utility import fill


def set_course_nodes(courses):
    '''
    A course generates as many nodes as the maximum number of attendees.

    Returns:
        The total number of nodes.
    '''
    node = 0
    for course in courses:
        to = node + course.max_students
        course.nodes = range(node, to)
        node = to
    return node


def create_costs(students, courses, node_count):
    costs = []
    for student in students:
        # Originally populate wiht 'NA'
        cost = fill(node_count, 'NA')
        for node in range(node_count):
            course = get_course(courses, node)
            if course.id in student.courses:
                # The cost is proportional to the position of the course in the prioritized list:
                # the higher the index, the higher the cost.
                cost[node] = student.courses.index(course.id)
        costs.append(cost)
    # If I do NOT have enough students, we will add some ghost students with maximum cost (here '1000') for each course.
    # They should be taken as last.
    diff = node_count - len(students)
    if diff > 0:
        print "There are more course seats than students. We need %d ghost participants." % diff
        max_cost = fill(node_count, 1000)
        for i in range(diff):
            costs.append(max_cost)
    return costs


def get_course(courses, node):
    '''
    For given node returns corresponding course.

    To each course have been allocated some node numbers.
    '''
    filtered = filter(lambda course: node in course.nodes, courses)
    return filtered[0]


def get_student(students, index):
    '''
    Returns the student found at given index.
    '''
    return students[index] if index < len(students) else None


# Taken from 'https://developers.google.com/optimization/assignment/simple_assignment'
def main():
    courses = load_courses()
    # Set 'nodes' property for each course.
    node_count = set_course_nodes(courses)
    students = load_students()
    student_count = len(students)
    if (student_count > node_count):
        print 'We do NOT have enough course places: %d < %d!' % (node_count, student_count)
        sys.exit(0)
    costs = create_costs(students, courses, node_count)
    # Students
    rows = len(costs)
    # Courses
    cols = len(costs[0])
    assignment = pywrapgraph.LinearSumAssignment()
    for student in range(rows):
        for course in range(cols):
            if costs[student][course] != 'NA':
                assignment.AddArcWithCost(student, course, costs[student][course])
    solve_status = assignment.Solve()
    if solve_status == assignment.OPTIMAL:
        print 'Total cost = %d' % assignment.OptimalCost()
        print
        for i in range(0, assignment.NumNodes()):
            crse = get_course(courses, assignment.RightMate(i))
            std = get_student(students, i)
            # If student NOT found, then this is a ghost one, no need to consider
            if std is not None:
                crse.add_student(std)
                print "Student '%s' assigned to course '%s' (%d). Cost = %d." % (
                    std.name, crse.title, crse.id, assignment.AssignmentCost(i))
        print
        for course in courses:
            print "Course '%s' (%d) has %d participant(s)." % (course.title, course.id, len(course.students))
    elif solve_status == assignment.INFEASIBLE:
        print 'No assignment is possible.'
    elif solve_status == assignment.POSSIBLE_OVERFLOW:
        print 'Some input costs are too large and may cause an integer overflow.'
    print
    print 'Finished!'


if __name__ == '__main__':
    main()
