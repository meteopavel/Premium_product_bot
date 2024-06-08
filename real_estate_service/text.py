from collections import namedtuple

# Declaring namedtuple()
Student = namedtuple('Student', ['name', 'age', 'DOB'])


def hello(smth):
    print(smth)


# Adding values
first = Student('Nandini', '19', hello)
second = Student('Nandini2', '12', hello)
students = (first, second)
for s in students:
    s.DOB(s.name)
