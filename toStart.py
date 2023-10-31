import os

with open("requirments.txt") as file:
    for string in file:
        res = os.system(string)
