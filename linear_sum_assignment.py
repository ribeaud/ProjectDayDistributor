from __future__ import division

import os
import sys
import logging
import numpy as np

from ortools.graph import pywrapgraph
from enum import Enum

from loader import CsvLoader, DbLoader
from utility import fill
from writer import ExcelWriter, ConsoleWriter

class Env(Enum):
    DEV = 1
    PROD = 2

def init_logging(env):
    format = '%(asctime)s %(levelname)s %(message)s'
    if (env is Env.PROD):
        logging.basicConfig(level=logging.DEBUG, format=format, filename=os.path.splitext(os.path.basename(__file__))[0] + '.log', filemode='w')
    else:
        logging.basicConfig(level=logging.DEBUG, format=format)
    return logging.getLogger(__name__)

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
        # Originally populate with 'NA'
        cost = fill(node_count, 'NA')
        for node in range(node_count):
            course = get_course(courses, node)
            if course.id in student.courses:
                # The cost is proportional to the position of the course in the prioritized list:
                # the higher the index, the higher the cost, multiplied by course cost. When the index
                # is zero, then there is no reason that the course does NOT get selected if we still
                # have some free seats.
                cost[node] = student.courses.index(course.id) * course.cost
        costs.append(cost)
    # If I do NOT have enough students, we will add some ghost students with maximum cost (here '1000') for each course.
    # They should be taken as last.
    diff = node_count - len(students)
    if diff > 0:
        logger.warning("There are more course seats (%d) than students (%d). We need %d ghost participants.", node_count, len(students), diff)
        max_cost = fill(node_count, 1000)
        for i in range(diff):
            costs.append(max_cost)
    np.set_printoptions(linewidth=sys.maxint)
    logger.debug("The cost matrix looks as following: %s.", np.matrix(costs))
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
    Returns the student found at given index, None otherwise (if given index out of range).
    '''
    return students[index] if index < len(students) else None

# Taken from 'https://developers.google.com/optimization/assignment/simple_assignment'
def main():
    courses = loader.load_courses()
    # Set 'nodes' property for each course.
    node_count = set_course_nodes(courses)
    # Set cost for each course: the higher 'max_students', the lower the cost
    m = max([course.max_students for course in courses])
    for course in courses:
        course.cost = m - course.max_students + 1
    # Load and sort the students
    students = sorted(loader.load_students(), key=lambda stu: stu.name)
    student_count = len(students)
    if student_count > node_count:
        logger.error('We do NOT have enough course places: %d < %d!', node_count, student_count)
        sys.exit(0)
    costs = create_costs(students, courses, node_count)
    # Students
    rows = len(costs)
    # Courses (or more exactly the number of course places)
    cols = len(costs[0])
    logger.info('The cost matrix has %dx%d dimension (students x course places).', rows, cols)
    assignment = pywrapgraph.LinearSumAssignment()
    for student in range(rows):
        for course in range(cols):
            # 'NA' means that the student is NOT interested in this course
            if costs[student][course] != 'NA':
                assignment.AddArcWithCost(student, course, costs[student][course])
    solve_status = assignment.Solve()
    if solve_status == assignment.OPTIMAL:
        logger.info('Total optimal cost is %d.', assignment.OptimalCost())
        for i in range(0, assignment.NumNodes()):
            crse = get_course(courses, assignment.RightMate(i))
            std = get_student(students, i)
            # If student NOT found, then this is a ghost one, no need to consider
            if std is not None:
                crse.add_student(std)
                std.course = crse
                std.cost = assignment.AssignmentCost(i)
        writer.write_courses(courses)
        writer.write_students(students, courses)
        writer.close()
    elif solve_status == assignment.INFEASIBLE:
        logger.error('No assignment is possible.')
    elif solve_status == assignment.POSSIBLE_OVERFLOW:
        logger.error('Some input costs are too large and may cause an integer overflow.')

if __name__ == '__main__':
    if len(sys.argv) and sys.argv[0] == 'PROD':
        env = Env.PROD
        logger = init_logging(env)
        loader = DbLoader(logger)
        writer = ExcelWriter(logger)
    else:
        env = Env.DEV
        logger = init_logging(env)
        loader = CsvLoader(logger)
        writer = ConsoleWriter(logger)
    main()
