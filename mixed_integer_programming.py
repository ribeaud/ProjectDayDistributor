from loader import CsvLoader

# Taken from 'https://developers.google.com/optimization/assignment/assignment_mip'
def main():
    loader = CsvLoader()
    courses = loader.load_courses()
    students = loader.load_students()

if __name__ == '__main__':
    main()