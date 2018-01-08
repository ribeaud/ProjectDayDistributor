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
        cost = fill(node_count, 'NA')
        for node in range(node_count):
            course = get_course(courses, node)
            if course.id in student.courses:
                # The cost is proportional to the position of the course in the prioritized list:
                # the higher the index, the higher the cost.
                cost[node] = student.courses.index(course.id)
        costs.append(cost)
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
    return students[index]

# Taken from 'https://developers.google.com/optimization/assignment/simple_assignment'
def main():
    courses = load_courses()
    # Set 'nodes' property for each course.
    node_count = set_course_nodes(courses)
    students = load_students()
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