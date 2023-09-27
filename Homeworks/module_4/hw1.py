"""
Create classes to track homeworks.

1. Homework - accepts howework text and deadline (datetime.timedelta)
Homework has a method, that tells if deadline has passed.

2. Student - can solve homework with `do_homework` method.
Raises DeadlineError with "You are late" message if deadline has passed

3. Teacher - can create homework with `create_homework`; check homework with `check_homework`.
Any teacher can create or check any homework (even if it was created by one of colleagues).

Homework are cached in dict-like structure named `homework_done`. Key is homework, values are 
solutions. Each student can only have one homework solution.

Teacher can `reset_results` - with argument it will reset results for specific homework, without -
it clears the cache.

Homework is solved if solution has more than 5 symbols.

-------------------
Check file with tests to see how all these classes are used. You can create any additional classes 
you want.
"""
from datetime import datetime, timedelta
from dataclasses import dataclass
from collections import defaultdict


@dataclass(eq=True, unsafe_hash=True)
class Homework:
    text: str
    deadline: int
    start_time: datetime

    def __init__(self, text: str, deadline: int):
        self.start_time = datetime.now()
        self.deadline = deadline
        self.text = text

    def is_deadline_passed(self):
        return not (self.start_time + timedelta(days=self.deadline)) > datetime.now()


@dataclass
class Student:
    surname: str
    name: str
    homework: Homework

    def __init__(self, surname: str, name: str):
        self.surname = surname
        self.name = name

    def do_homework(self, homework: Homework, result: str):
        self.homework = homework
        if (homework.is_deadline_passed()):
            raise DeadlineError("You are late")
        return Solution(self, result)


@dataclass
class Solution:
    author: Student
    result: str

    def is_solved(self):
        return len(self.result) > 5


@dataclass
class Teacher:
    surname: str
    name: str
    homework_done: dict

    def __init__(self, surname: str, name: str):
        self.surname = surname
        self.name = name
        if (not hasattr(Teacher, "homework_done")):
            Teacher.homework_done = defaultdict(list)

    @staticmethod
    def create_homework(homework: str, deadline: int):
        return Homework(homework, deadline)

    @classmethod
    def check_homework(cls, solution: Solution):
        solutions = Teacher.homework_done[solution.author.homework]
        if solution not in solutions and solution.is_solved():
            solutions.append(solution)
        return solution.is_solved()

    @classmethod
    def reset_results(cls, *args):
        if (len(args) == 0):
            Teacher.homework_done.clear()
        else:
            Teacher.homework_done.pop(args[0])


class DeadlineError(Exception):
    """"Exception for failed deadline"""
