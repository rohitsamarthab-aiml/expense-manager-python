import csv
import os

FILE_NAME = "expenses.csv"

def initialize_file():
    """Creates the file with headers if it doesn't exist."""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Item", "Amount", "Category"])

def save_expense(date, item, amount, category):
    """Saves a single expense to the CSV file."""
    initialize_file()
    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, item, amount, category])

def load_expenses():
    """Reads all expenses from the CSV file."""
    initialize_file()
    expenses = []
    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if row: # Ensure no empty lines are read
                expenses.append(row)
    return expenses

def delete_expense(index):
    """Deletes an expense at a specific index."""
    expenses = load_expenses()
    if 0 <= index < len(expenses):
        del expenses[index]
        # Re-write the file with the updated list
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Item", "Amount", "Category"]) # Header
            writer.writerows(expenses)