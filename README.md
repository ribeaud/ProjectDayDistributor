# Project Day Distributor

Main program is `linear_sum_assignment.py`. It will distribute/dispatch the students according
to their given prioritized list.

## loader.py

There are two kinds of data loader: `CsvLoader` and `DbLoader`. Customize the latter
one to your specific needs to access your database.

The `CsvLoader` reads in two **CSV** files, `courses.txt` and `students.txt`
which MUST have following format:

#### courses.txt
```
id	title	max_students
0	Course 0	4
1	Course 1	2
2	Course 2	1
...
```

#### students.txt
```
name	prioritized_list
Philomène	3,2,0
Phénicia	1,9,0
Tanja	2,4,1
...
```

## writer.py

There are two kinds of data output writer: `ExcelWriter`, `ConsoleWriter`.

`ConsoleWriter` outputs the following:
```
Total cost = 20002
Student 'Student 11' assigned to course 'Course 10' (9). Cost = 0.
Student 'Student 4' assigned to course 'Course 9' (8). Cost = 1.
Student 'Student 8' assigned to course 'Course 9' (8). Cost = 0.
Student 'Philomène' assigned to course 'Course 4' (3). Cost = 0.
...
```

## Environment

With a program argument, you specify in which mode you want to work:

```python
if len(argv) > 1 and argv[1] == 'PROD':
    env = Env.PROD
    logger = init_logging(env)
    loader = DbLoader(logger)
    writer = ExcelWriter(logger)
else:
    env = Env.DEV
    logger = init_logging(env)
    loader = CsvLoader(logger)
    writer = ConsoleWriter(logger)

```

## Links

- https://developers.google.com/optimization/assignment/simple_assignment
- https://developers.google.com/optimization/assignment/assignment_mip

## Assumptions

- Nothing happens if we do NOT have enough seats available for all the students.
- Students are deeply shuffled after loading. Because the first student gets
his first specified seat.
- Courses providing more seats have a _lower_ cost.