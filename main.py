from itertools import repeat

from ortools.graph import pywrapgraph
from parser import default_read_and_filter_csv

class Course:
    '''
    A course. A course has an unique ID (a number), a title and a maximum number of participants.
    For each possible participant, we should have a numbered node. And first come first serve. It means, the cost
    should be higher for the final participants.
    '''
    def __init__(self, id, title, max_participants):
        self.id = id
        self.title = title
        self.free = self.max_participants = max_participants

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
    for line in lines:
        courses.append(Course(int(line['id']), line['title'], line['max_participants']))
    courses.sort(key=lambda course: course.id)
    return courses

def load_participants():
    participants = []
    lines = default_read_and_filter_csv('participants.txt')
    index = 0
    for line in lines:
        participants.append(Participant(index, line['name'], line['prioritized_list']))
        index += 1
    return participants

def create_cost_array(participants, courses_length):
    cost = []
    for participant in participants:
        temp = fill(courses_length, 'NA')
        # Assuming we go over all the courses this way
        for course in range(courses_length):
            if course in participant.courses:
                temp[course] = participant.courses.index(course)
        cost.append(temp)
    return cost

def fill(length, value):
    return list(repeat(value, length))

def main():
    courses = load_courses()
    participants = load_participants()
    cost = create_cost_array(participants, len(courses))
    print cost
    rows = len(cost)
    cols = len(cost[0])
    assignment = pywrapgraph.LinearSumAssignment()
    for worker in range(rows):
        for task in range(cols):
            if cost[worker][task] != 'NA':
                assignment.AddArcWithCost(worker, task, cost[worker][task])
    solve_status = assignment.Solve()
    if solve_status == assignment.OPTIMAL:
        print 'Total cost = %d' % assignment.OptimalCost()
        print
        for i in range(0, assignment.NumNodes()):
            print 'Worker %d assigned to task %d. Cost = %d' % (i, assignment.RightMate(i), assignment.AssignmentCost(i))
    elif solve_status == assignment.INFEASIBLE:
        print 'No assignment is possible.'
    elif solve_status == assignment.POSSIBLE_OVERFLOW:
        print 'Some input costs are too large and may cause an integer overflow.'
    print 'Finished!'

if __name__ == '__main__':
    main()
