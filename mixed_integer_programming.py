from loader import load_courses, load_students

# Taken from 'https://developers.google.com/optimization/assignment/assignment_mip'
def main():
    courses = load_courses()
    students = load_students()

if __name__ == '__main__':
    main()