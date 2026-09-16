from chunker import remove_table_of_contents


text = """
Project Introduction

Contents

Introduction ........ 1
Problem Stated ....... 2
System as a Solution . 3
Risk Management ...... 4

Introduction

This project aims to solve a real problem.
It provides an academic environment for students.
"""

result = remove_table_of_contents(text)

print(result)