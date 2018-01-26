# Project Day Distributor
This **Python** project read in two CSV files, `courses.txt` and `students.txt`
which must have following format:

## courses.txt
```
id	title	max_students
0	Course 0	4
1	Course 1	2
2	Course 2	1
...
```

## students.txt
```
name	prioritized_list
Philomène	3,2,0
Phénicia	1,9,0
Tanja	2,4,1
...
```
Main programs are `linear_sum_assignment.py`
and `mixed_integer_programming.py`. They will dispatch the students according
to their given prioritized list.

For example, running `python linear_sum_assignment.py` outputs the following:
```
Total cost = 20002
Student 'Student 11' assigned to course 'Course 10' (9). Cost = 0.
Student 'Student 4' assigned to course 'Course 9' (8). Cost = 1.
Student 'Student 8' assigned to course 'Course 9' (8). Cost = 0.
Student 'Philomène' assigned to course 'Course 4' (3). Cost = 0.
...
```

## Links

- https://developers.google.com/optimization/assignment/simple_assignment
- https://developers.google.com/optimization/assignment/assignment_mip

## Assumptions

- Nothing happens if we do NOT have enough seats available for all the students.
- Students are deeply shuffled after loading. Because the first student gets
his first specified seat.
- Courses providing more seats have a lower cost.