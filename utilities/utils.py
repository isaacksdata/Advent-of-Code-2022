from dotenv import dotenv_values
from aocd import get_data, submit
import re


def get_session():
    return dotenv_values()["AOC_SESSION"]


def get_puzzle(year: int, day: int):
    return get_data(session=get_session(), day=day, year=year)


def submit_answer(answer, part: str, day: int, year: int):
    submit(answer, part=part, day=day, year=year, session=get_session())


def read_sample_data(day: int):
    path = f"../data/sample_{day}.txt"
    with open(path, 'r') as file:
        # Read the contents of the file into a list
        data = file.readlines()
    data = [x.replace("\n", "") for x in data]
    return data


def extract_numbers(string):
    # Use a regular expression to find all numbers in the string
    matches = re.finditer(r'-?\d+', string)

    # Extract the numbers from the matches
    numbers = [int(match.group()) for match in matches]
    return numbers

