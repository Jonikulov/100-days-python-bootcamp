"""Day 26. Python Comprehensions. The NATO Alphabet"""

import pandas
import random

student_dict = {
    "student": ["Angela", "James", "Lily"], 
    "score": [56, 76, 98]
}

# Looping through dictionaries:
for (key, value) in student_dict.items():
    # Access key and value
    print(key, value)
print()

student_data_frame = pandas.DataFrame(student_dict)
# Loop through rows of a data frame
for (index, row) in student_data_frame.iterrows():
    # Access index and row
    # Access row.student or row.score
    print(index, row.student, row.score)
print()

names = ["Alex", "Beth", "Caroline", "Dave", "Eleanor", "Freddie"]
student_scores = {name: random.randint(1, 100) for name in names}
print(student_scores)
passed_students = {
    name: score for (name, score) in student_scores.items() if score > 60
}
print(passed_students)
