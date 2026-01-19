import tkinter as tk
from tkinter import ttk  # <--- 1. ADD THIS IMPORT
from tkinter import messagebox
import backend

class AddExpenseFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller

        tk.Label(self, text="Add New Expense", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333").pack(pady=20)

        form_frame = tk.Frame(self, bg="#f0f0f0")
        form_frame.pack(pady=10)

        # Date
        tk.Label(form_frame, text="Date (YYYY-MM-DD):", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_date = tk.Entry(form_frame, width=25)
        self.entry_date.grid(row=0, column=1, padx=10, pady=5)

        # Item
        tk.Label(form_frame, text="Item Name:", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_item = tk.Entry(form_frame, width=25)
        self.entry_item.grid(row=1, column=1, padx=10, pady=5)

        # Amount
        tk.Label(form_frame, text="Amount:", bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_amount = tk.Entry(form_frame, width=25)
        self.entry_amount.grid(row=2, column=1, padx=10, pady=5)

        # --- 2. THIS IS WHERE YOU ADD THE CATEGORIES ---
        tk.Label(form_frame, text="Category:", bg="#f0f0f0").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        
        # List your categories here
        categories = ["Rent", "Food", "Transportation", "Fees", "Personal", "Medicines", "Clothes", "Other"]
        
        # Use Combobox instead of Entry
        self.entry_category = ttk.Combobox(form_frame, values=categories, width=23, state="readonly")
        self.entry_category.grid(row=3, column=1, padx=10, pady=5)
        self.entry_category.current(0) # Selects 'Rent' by default
        # -----------------------------------------------

        btn_frame = tk.Frame(self, bg="#f0f0f0")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Save Expense", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                  command=self.submit_expense).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="Back to Home", command=lambda: controller.show_frame("HomeFrame")).pack(side=tk.LEFT, padx=10)

    def submit_expense(self):
        date = self.entry_date.get()
        item = self.entry_item.get()
        amount = self.entry_amount.get()
        category = self.entry_category.get() # This now gets the selected value from the dropdown

        if date and item and amount and category:
            backend.save_expense(date, item, amount, category)
            messagebox.showinfo("Success", "Expense Added Successfully!")
            self.clear_entries()
        else:
            messagebox.showwarning("Error", "Please fill all fields")

    def clear_entries(self):
        self.entry_date.delete(0, tk.END)
        self.entry_item.delete(0, tk.END)
        self.entry_amount.delete(0, tk.END)
        self.entry_category.set(self.entry_category['values'][0]) # Reset dropdown to first item