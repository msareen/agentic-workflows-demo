# quick_python_primer.py

# ----------------------------------------
# 🔹 INTERFACE-LIKE STRUCTURE
# ----------------------------------------
from abc import ABC, abstractmethod
import os

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def area(self):
        return 3.14 * 5 * 5

print("Circle Area:", Circle().area())

# ----------------------------------------
# 🔹 GENERATOR FUNCTION
# ----------------------------------------
def counter(n):
    for i in range(n):
        yield i

for val in counter(3):
    print("Yielded:", val)

# ----------------------------------------
# 🔹 VARIABLE SCOPE
# ----------------------------------------
x = "global"

def show_scope():
    y = "local"
    print("Inside:", x, y)

show_scope()
# print(y)  # ❌ Error: y is not defined outside

# ----------------------------------------
# 🔹 FUNCTION SCOPE
# ----------------------------------------
def scoped():
    msg = "hidden"
scoped()
# print(msg)  # ❌ Error: msg not accessible here

# ----------------------------------------
# 🔹 IMPORT / FROM STATEMENT
# ----------------------------------------
from math import sqrt
print("Sqrt of 25:", sqrt(25))

# ----------------------------------------
# 🔹 TYPING_EXTENSIONS & ANNOTATED
# ----------------------------------------
from typing_extensions import TypedDict, Annotated
from typing import Literal

# ➤ Annotated for basic validation use
def check_age(age: Annotated[int, "must be >= 18"]):
    if age < 18:
        raise ValueError("Too young")
    print("Age OK")

check_age(20)

# ➤ TypedDict with Annotated
class User(TypedDict):
    name: Annotated[str, "Full name"]
    age: Annotated[int, "Age >= 0"]

u: User = {"name": "Alice", "age": 30}
print("User:", u)

# ➤ Annotated + Literal
Choice = Annotated[Literal["yes", "no"], "Only yes/no allowed"]

def choose_static(c: Choice):
    print("Choice is:", c)

choose_static("maybe")
# choose("maybe")  # ❌ Type checker will warn

# How to inforce 

from pydantic import BaseModel, ValidationError
from typing import Literal

class ChoiceModel(BaseModel):
    choice: Literal["yes", "no"]

def choose(c: str):
    try:
        model = ChoiceModel(choice=c)
        print("Choice is:", model.choice)
    except ValidationError as e:
        print("Invalid choice:", e)

# choose("maybe")  # Will raise a validation error
choose("yes") 

# Done ✅
