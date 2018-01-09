class Course:
    '''
    A course has an unique ID (a number), a title and a maximum number of participants (students).

    For each possible student/place, we should have a numbered node. First come first serve: it means, the cost
    should be higher for the final students.
    '''

    def __init__(self, id, title, max_students):
        self.id = id
        self.title = title
        self.max_students = max_students

    def __repr__(self):
        return str(self.__class__.__name__) + ": " + str(self.__dict__)


class Student:
    '''
    A student (or course participant). It has an ID, a name and a list of courses in which he is interested.

    The ID is used as node ID and must be positive.
    '''

    def __init__(self, id, name, courses):
        assert id > -1, "%d MUST be positive" % (id)
        self.id = id
        self.name = name
        self.courses = [int(course) for course in courses.split(',')] if courses is not None else []

    def __repr__(self):
        return str(self.__class__.__name__) + ": " + str(self.__dict__)
