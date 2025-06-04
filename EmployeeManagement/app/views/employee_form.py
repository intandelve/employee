import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import Toplevel, Label, StringVar, messagebox

from app.config import get_all_departments, add_employee, update_employee


class EmployeeForm(Toplevel):
    """
    Add / Edit employee pop-up.
    Combobox is populated with department names fetched from MySQL.
    """
    def __init__(self, master, mode="add", employee_data=None, refresh_callback=None):
        super().__init__(master)

        # -------- basic window settings --------
        self.title("Add Employee" if mode == "add" else "Edit Employee")
        self.geometry("420x310")
        self.resizable(False, False)

        self.mode = mode
        self.employee_data = employee_data      # tuple: (id, name, position, department, status)
        self.refresh_callback = refresh_callback

        # -------- Tkinter variables --------
        self.name_var       = StringVar()
        self.position_var   = StringVar()
        self.department_var = StringVar()
        self.status_var     = StringVar()

        # List of (id, name) tuples from DB
        self.departments = []

        # Build UI widgets, then load departments from DB
        self._create_widgets()
        self._load_departments()

        # If edit mode, pre-fill the fields
        if self.mode == "edit" and self.employee_data:
            self._populate_fields()

    # ------------------------------------------------------------------ #
    #  W I D G E T S
    # ------------------------------------------------------------------ #
    def _create_widgets(self):
        self.configure(padx=20, pady=20)
        title = "Add New Employee" if self.mode == "add" else "Edit Employee"
        Label(self, text=title, font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        pad = {'padx': 10, 'pady': 5}

        tb.Label(self, text="Full Name:", bootstyle="secondary").grid(row=1, column=0, sticky="e", **pad)
        tb.Entry(self, textvariable=self.name_var, width=30).grid(row=1, column=1, **pad)

        tb.Label(self, text="Position:", bootstyle="secondary").grid(row=2, column=0, sticky="e", **pad)
        tb.Entry(self, textvariable=self.position_var, width=30).grid(row=2, column=1, **pad)

        tb.Label(self, text="Department:", bootstyle="secondary").grid(row=3, column=0, sticky="e", **pad)
        self.cb_department = tb.Combobox(self, textvariable=self.department_var, state="readonly", width=28)
        self.cb_department.grid(row=3, column=1, **pad)

        tb.Label(self, text="Status:", bootstyle="secondary").grid(row=4, column=0, sticky="e", **pad)
        tb.Entry(self, textvariable=self.status_var, width=30).grid(row=4, column=1, **pad)

        btn_text = "Add Employee" if self.mode == "add" else "Update Employee"
        btn_style = "success" if self.mode == "add" else "warning"

        tb.Button(
            self,
            text=btn_text,
            bootstyle=f"{btn_style} outline",
            width=25,
            command=self._submit_form
        ).grid(row=5, column=0, columnspan=2, pady=20)

    # ------------------------------------------------------------------ #
    #  D A T A   H E L P E R S
    # ------------------------------------------------------------------ #
    def _load_departments(self):
        """
        Pull department list from DB and feed the Combobox.
        Assumes get_all_departments() returns rows like (id, department_name, manager)
        """
        try:
            rows = get_all_departments()
            self.departments = [(r[0], r[1]) for r in rows]           # keep ID if needed
            dep_names = [d[1] for d in self.departments]

            self.cb_department["values"] = dep_names
            if dep_names:
                self.cb_department.current(0)                         # pre-select first item
        except Exception as e:
            print("Error loading departments:", e)
            self.departments = []
            self.cb_department["values"] = []

    def _populate_fields(self):
        """Fill entries & combobox with existing employee data (tuple order must match)."""
        self.name_var.set(self.employee_data[1])
        self.position_var.set(self.employee_data[2])
        self.status_var.set(self.employee_data[4])

        current_dep = self.employee_data[3]
        try:
            index = [d[1] for d in self.departments].index(current_dep)
            self.cb_department.current(index)
        except ValueError:
            # department no longer exists … leave combobox as-is
            pass

    # ------------------------------------------------------------------ #
    #  S U B M I T
    # ------------------------------------------------------------------ #
    def _submit_form(self):
        name       = self.name_var.get().strip()
        position   = self.position_var.get().strip()
        department = self.department_var.get().strip()   # chosen name from combobox
        status     = self.status_var.get().strip()

        if not all([name, position, department, status]):
            messagebox.showwarning("Missing Data", "Please complete every field.")
            return

        if self.mode == "add":
            ok = add_employee(name, position, department, status)
        else:
            emp_id = self.employee_data[0]
            ok = update_employee(emp_id, name, position, department, status)

        if ok:
            messagebox.showinfo("Success", f"Employee {'added' if self.mode=='add' else 'updated'} successfully.")
            self.destroy()
            if self.refresh_callback:
                self.refresh_callback()
        else:
            messagebox.showerror("Error", "Database operation failed.")


# ---------------------------------------------------------------------- #
#  Quick manual test (run this file directly)
# ---------------------------------------------------------------------- #
if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()

    # Example: (id, name, position, department, status)
    # data = (1, "Alice", "Manager", "Finance", "Active")
    EmployeeForm(root, mode="add").mainloop()
