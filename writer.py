import xlsxwriter

def writeCourses(courses):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('assignment.xlsx')
    worksheet = workbook.add_worksheet('Courses')
    bold = workbook.add_format({'bold': True})

    col = 0

    # Iterate over the data and write it out row by row.
    for course in courses:
        row = 0
        worksheet.write(row, col, course.title, bold)
        row += 1
        students = sorted(course.students, key=lambda stu: stu.name)
        for student in students:
            worksheet.write(row, col, student.name)
            row += 1
        col += 1

    workbook.close()