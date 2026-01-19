import tkinter as tk
from add_ui import AddExpenseFrame  # Linking Member 2
from view_ui import ViewExpenseFrame # Linking Member 3

class ExpenseManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Team Expense Manager")
        self.geometry("500x500")
        self.configure(bg="#f0f0f0")

        # Container to stack frames
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        # Initialize all frames
        for F in (HomeFrame, AddExpenseFrame, ViewExpenseFrame):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomeFrame")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()

class HomeFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller

        tk.Label(self, text="Expense Manager", font=("Helvetica", 24, "bold"), bg="#f0f0f0", fg="#2c3e50").pack(pady=50)

        tk.Button(self, text="Add New Expense", font=("Arial", 14), bg="#4CAF50", fg="white", width=20,
                  command=lambda: controller.show_frame("AddExpenseFrame")).pack(pady=10)

        tk.Button(self, text="View Expenses", font=("Arial", 14), bg="#2196F3", fg="white", width=20,
                  command=lambda: controller.show_frame("ViewExpenseFrame")).pack(pady=10)

        tk.Button(self, text="Exit", font=("Arial", 12), bg="#e74c3c", fg="white", width=10,
                  command=controller.quit).pack(pady=30)

if __name__ == "__main__":
    app = ExpenseManagerApp()
    app.mainloop()