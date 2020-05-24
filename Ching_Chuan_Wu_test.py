import os
from threading import Thread

import QuestionA
import QuestionB

# Test case for Question A
print("Testing Question A. Please refer to Readme file for explanation of each test case")
f = None
try:
    f = open('QuestionA.txt')
except FileNotFoundError:
    pass
if f:
    test_cases_number = int(f.readline().strip())
    for i in range(test_cases_number):
        first_line_start, first_line_end = f.readline().strip().split(" ")
        second_line_start, second_line_end = f.readline().strip().split(" ")
        expected = bool(int(f.readline().strip()))
        print("Testing with line (" +
              first_line_start + "," + first_line_end +
              ") and line (" +
              second_line_start + "," + second_line_end + ")")
        overlap = QuestionA.overlap((float(first_line_start),float(first_line_end)),(float(second_line_start),float(second_line_end)))
        # This assertion must pass
        assert overlap == expected
        if overlap:
            print("They overlap!")
        else:
            print("They don't overlap")
else:
    print("QuestionA.txt not provided and test skipped. Please provide the file in the format explained in Readme file")
f.close()
print(" ")
print(" ")

# Test case for Question B
print("Testing Question B. Please refer to Readme file for explanation of each test case")
f = None
try:
    f = open('QuestionB.txt')
except FileNotFoundError:
    pass
if f:
    test_cases_number = int(f.readline().strip())
    for i in range(test_cases_number):
        a, b = f.readline().strip().split(" ")
        result = f.readline().strip()
        print("Testing with a = " + a + " and b = " + b)
        equality = QuestionB.greaterthan(a, b)
        # This assertion must pass
        assert equality == result
        if equality=="equal":
            print("a is equal to b")
        elif equality=="greater":
            print("a is greater than b")
        elif equality=="less":
            print("a is less than b")
        else:
            print("Wrong input format. Please enter string that start with number or -/+ sign and only include number after the first character for the first or second input or both")
else:
    print("QuestionB.txt not provided and test skipped. Please provide the file in the format explained in Readme file")
f.close()
print(" ")
print(" ")

# Test case for Question C
print("Testing Question C")
# Helper to execute any python program given program name
def run_program(program_name):
    os.system('python ' + program_name)
t1 = Thread(target=run_program, args=('server1.py',))
t1.start()
t1.join()
