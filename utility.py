from itertools import repeat


def fill(length, value):
    return list(repeat(value, length))

def sort_students(students):
    '''
    Sorts students by his level first, then by his name
    '''
    def by_level_and_name(student):
        return (student.level, student.name) if hasattr(student, 'level') else student.name

    return sorted(students, key=by_level_and_name)
