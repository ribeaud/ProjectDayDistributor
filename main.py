import unicodecsv as csv
from ortools.graph import pywrapgraph

class Course:
    def __init__(self, id, title, maxParticipants):
        self.id = id
        self.title = title
        self.maxParticipants = maxParticipants

    def __repr__(self):
        return str(self.__class__.__name__) + ": " + str(self.__dict__)

class Participant:
    def __init__(self, name, courses):
        self.name = name
        self.courses = [int(course) for course in courses.split(',')]

    def __repr__(self):
        return str(self.__class__.__name__) + ": " + str(self.__dict__)

def load_courses():
    courses = []
    with open('courses.txt', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        # Ignore header
        reader.next()
        for row in reader:
            courses.append(Course(int(row[0]), row[1], row[2]))
    return courses

def load_participants():
    participants = []
    with open('participants.txt', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        # Ignore header
        reader.next()
        for row in reader:
            participants.append(Participant(row[0], row[1]))
    return participants

def main():
    courses = load_courses()
    participants = load_participants()
    min_cost_flow = pywrapgraph.SimpleMinCostFlow()
    print 'Hello'

if __name__ == '__main__':
    main()
