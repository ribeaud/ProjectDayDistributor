import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost', user='root', password='', db='ogw', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

def load_courses():
    pass

def load_students():
    pass