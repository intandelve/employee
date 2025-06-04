import ttkbootstrap as tb
from tkinter import Toplevel, StringVar, messagebox
import tkinter as tk
from ttkbootstrap.constants import *
from app.config import add_department, update_department

class DepartmentForm(tk.Toplevel):
    def __init__(self, master, parent_view, title, dep_id=None, department_name="", manager=""):
        super().__init__(master)
        self.parent_view = parent_view
        self.dep_id = dep_id
        self.title(title)

        # Set window size and center position
        window_width = 480
        window_height =420
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)
        self.configure(bg="white")

        self.var_department_name = StringVar(value=department_name)
        self.var_manager = StringVar(value=manager)

        self.build_ui()

    def build_ui(self):
        frm = tb.Frame(self, padding=20, bootstyle="light")
        frm.pack(fill="both", expand=True, padx=20, pady=20)

        title_label = tb.Label(frm, text="Department Details", font=("Segoe UI", 16, "bold"))
        title_label.pack(anchor="center", pady=(0, 20))

        # Department Name
        name_label = tb.Label(frm, text="Department Name:", font=("Segoe UI", 10))
        name_label.pack(anchor="w", pady=(0, 5))
        self.entry_department_name = tb.Entry(frm, textvariable=self.var_department_name, font=("Segoe UI", 10))
        self.entry_department_name.pack(fill="x", pady=(0, 15))

        # Manager
        manager_label = tb.Label(frm, text="Manager:", font=("Segoe UI", 10))
        manager_label.pack(anchor="w", pady=(0, 5))
        self.entry_manager = tb.Entry(frm, textvariable=self.var_manager, font=("Segoe UI", 10))
        self.entry_manager.pack(fill="x", pady=(0, 15))

        # Add/Update Button
        btn_text = "Update" if self.dep_id else "Add"
        btn = tb.Button(
            frm,
            text=btn_text,
            bootstyle="success",
            command=self.submit,
            width=30,
            padding=(5, 10)
        )
        btn.pack(pady=(10, 0))

    def submit(self):
        department_name = self.var_department_name.get().strip()
        manager = self.var_manager.get().strip()

        if not department_name:
            messagebox.showwarning("Validation Error", "Department name cannot be empty.")
            return

        if self.dep_id:
            success = update_department(self.dep_id, department_name, manager)
            action = "updated"
        else:
            success = add_department(department_name, manager)
            action = "added"

        if success:
            messagebox.showinfo("Success", f"Department {action} successfully.")
            self.parent_view.load_departments()
            self.destroy()
        else:
            messagebox.showerror("Error", f"Failed to {action} department.")
