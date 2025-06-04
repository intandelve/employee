import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox

from .employee_form import EmployeeForm  # Pastikan kamu punya file ini
from ..config import get_all_employees, delete_employee


class EmployeeView(tb.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self.master = master
        self.build_ui()
        self.load_employees()

    def build_ui(self):
        title = tb.Label(self, text="Employee Data", font=("Segoe UI", 16, "bold"))
        title.pack(anchor="w", pady=(0, 10))

        table_frame = tb.Frame(self)
        table_frame.pack(fill="both", expand=True)

        vsb = tb.Scrollbar(table_frame, orient="vertical")
        vsb.pack(side="right", fill="y")

        hsb = tb.Scrollbar(table_frame, orient="horizontal")
        hsb.pack(side="bottom", fill="x")

        self.tree = tb.Treeview(
            table_frame,
            columns=("ID", "Name", "Position", "Department", "Status"),
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=15,
            style="info.Treeview"
        )
        self.tree.pack(fill="both", expand=True)

        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)

        for col, width, anchor in [
            ("ID", 50, "center"),
            ("Name", 180, "w"),
            ("Position", 150, "w"),
            ("Department", 150, "w"),
            ("Status", 100, "center")
        ]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=anchor)

        self.tree.tag_configure('oddrow', background='#d0ebff')
        self.tree.tag_configure('evenrow', background='white')

        btn_frame = tb.Frame(self)
        btn_frame.pack(fill="x", pady=(10, 0))

        tb.Button(btn_frame, text="Add Employee", bootstyle="primary", command=self.add_employee).pack(side="left", padx=5)
        tb.Button(btn_frame, text="Edit Selected", bootstyle="warning", command=self.edit_employee).pack(side="left", padx=5)
        tb.Button(btn_frame, text="Delete Selected", bootstyle="danger", command=self.delete_employee).pack(side="left", padx=5)

    def load_employees(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        employees = get_all_employees()
        for index, emp in enumerate(employees):
            tag = 'oddrow' if index % 2 == 0 else 'evenrow'
            self.tree.insert("", "end", values=emp, tags=(tag,))

    def add_employee(self):
        EmployeeForm(self, mode="add", refresh_callback=self.load_employees)

    def edit_employee(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select an employee to edit.")
            return
        data = self.tree.item(selected[0])["values"]
        EmployeeForm(self, mode="edit", employee_data=data, refresh_callback=self.load_employees)

    def delete_employee(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select an employee to delete.")
            return
        emp_id = self.tree.item(selected[0])["values"][0]
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this employee?")
        if confirm:
            success = delete_employee(emp_id)
            if success:
                messagebox.showinfo("Success", "Employee deleted successfully.")
                self.load_employees()
            else:
                messagebox.showerror("Error", "Failed to delete employee.")
