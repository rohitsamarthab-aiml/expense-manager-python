import tkinter as tk
from tkinter import ttk, messagebox
import backend
import matplotlib.pyplot as plt # For the Graph

class ViewExpenseFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller

        # --- Header ---
        tk.Label(self, text="Manage & Analyze Expenses", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333").pack(pady=10)

        # --- Table Section ---
        columns = ("Date", "Item", "Amount", "Category")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=8)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=90)

        self.tree.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)

        # --- Action Buttons (Delete & Refresh) ---
        btn_frame = tk.Frame(self, bg="#f0f0f0")
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Refresh List", command=self.load_data, bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete Selected", command=self.delete_selected, bg="#e74c3c", fg="white").pack(side=tk.LEFT, padx=5)

        # --- Analysis Section (Income & Savings) ---
        analysis_frame = tk.LabelFrame(self, text="Monthly Analysis", bg="#f0f0f0", font=("Arial", 10, "bold"))
        analysis_frame.pack(pady=10, padx=20, fill="x")

        # Income Input
        tk.Label(analysis_frame, text="Enter Monthly Income:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5)
        self.entry_income = tk.Entry(analysis_frame, width=15)
        self.entry_income.grid(row=0, column=1, padx=10, pady=5)
        
        # Calculate Button
        tk.Button(analysis_frame, text="Calculate Savings", command=self.calculate_savings, bg="#FF9800", fg="white").grid(row=0, column=2, padx=10, pady=5)

        # Results Labels
        self.lbl_total_expense = tk.Label(analysis_frame, text="Total Expense: 0", bg="#f0f0f0", font=("Arial", 10))
        self.lbl_total_expense.grid(row=1, column=0, padx=10, pady=5)

        self.lbl_savings = tk.Label(analysis_frame, text="Net Savings: 0", bg="#f0f0f0", font=("Arial", 10, "bold"))
        self.lbl_savings.grid(row=1, column=1, padx=10, pady=5)

        # Graph Button
        tk.Button(self, text="Show Expense Graph", command=self.show_graph, bg="#9C27B0", fg="white", font=("Arial", 12)).pack(pady=10)

        # Back Button
        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomeFrame")).pack(pady=5)

    def load_data(self):
        """Refreshes the table with data from backend"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        data = backend.load_expenses()
        for row in data:
            self.tree.insert("", tk.END, values=row)

    def delete_selected(self):
        """Deletes the selected row"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Error", "Please select an expense to delete")
            return

        # Get the index of the selected item
        index = self.tree.index(selected_item[0])
        
        # Call backend to delete
        backend.delete_expense(index)
        
        # Refresh UI
        self.load_data()
        messagebox.showinfo("Success", "Expense Deleted")

    def calculate_savings(self):
        """Calculates Total Expense and Savings based on Income"""
        income_str = self.entry_income.get()
        if not income_str.isdigit():
            messagebox.showerror("Error", "Please enter a valid numeric income")
            return
        
        income = float(income_str)
        expenses = backend.load_expenses()
        
        total_expense = 0
        for row in expenses:
            # row[2] is the Amount column
            total_expense += float(row[2])

        savings = income - total_expense

        self.lbl_total_expense.config(text=f"Total Expense: {total_expense}")
        self.lbl_savings.config(text=f"Net Savings: {savings}", fg="green" if savings >= 0 else "red")

    def show_graph(self):
        """Generates a Pie Chart of expenses by Category"""
        expenses = backend.load_expenses()
        if not expenses:
            messagebox.showinfo("Info", "No expenses to show")
            return

        category_totals = {}
        for row in expenses:
            category = row[3] # Category column
            amount = float(row[2]) # Amount column
            
            if category in category_totals:
                category_totals[category] += amount
            else:
                category_totals[category] = amount

        # Prepare data for plotting
        categories = list(category_totals.keys())
        amounts = list(category_totals.values())

        # Plotting
        plt.figure(figsize=(6, 6))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
        plt.title("Expense Distribution by Category")
        plt.show()

    def tkraise(self, aboveThis=None):
        self.load_data()
        super().tkraise(aboveThis)