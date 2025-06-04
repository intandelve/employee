import ttkbootstrap as tb
from ttkbootstrap.constants import *
from app.config import get_all_departments, add_department, update_department, delete_department
from tkinter import messagebox

from app.views.department_form import DepartmentForm


class DepartmentView(tb.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self.master = master
        self.build_ui()
        self.load_departments()

    def build_ui(self):
        title = tb.Label(self, text="Department Management", font=("Segoe UI", 16, "bold"))
        title.pack(anchor="w", pady=(0, 10))

        table_frame = tb.Frame(self)
        table_frame.pack(fill="both", expand=True)

        vsb = tb.Scrollbar(table_frame, orient="vertical")
        vsb.pack(side="right", fill="y")

        hsb = tb.Scrollbar(table_frame, orient="horizontal")
        hsb.pack(side="bottom", fill="x")

        self.tree = tb.Treeview(
            table_frame,
            columns=("ID", "Department Name", "Manager"),
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=15,
            style="success.Treeview"
        )
        self.tree.pack(fill="both", expand=True)

        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)

        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=50, anchor="center")

        self.tree.heading("Department Name", text="Department Name")
        self.tree.column("Department Name", width=200, anchor="w")

        self.tree.heading("Manager", text="Manager")
        self.tree.column("Manager", width=150, anchor="w")

        self.tree.tag_configure('oddrow', background='#e9e7fd')  # light purple
        self.tree.tag_configure('evenrow', background='white')

        btn_frame = tb.Frame(self)
        btn_frame.pack(fill="x", pady=(10, 0))

        btn_add = tb.Button(btn_frame, text="Add Department", bootstyle="success", command=self.add_department)
        btn_add.pack(side="left", padx=5)

        btn_edit = tb.Button(btn_frame, text="Edit Selected", bootstyle="warning", command=self.edit_department)
        btn_edit.pack(side="left", padx=5)

        btn_delete = tb.Button(btn_frame, text="Delete Selected", bootstyle="danger", command=self.delete_department)
        btn_delete.pack(side="left", padx=5)

    def load_departments(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        departments = get_all_departments()
        for index, dept in enumerate(departments):
            tag = 'oddrow' if index % 2 == 0 else 'evenrow'
            self.tree.insert("", "end", values=dept, tags=(tag,))

    def add_department(self):
        DepartmentForm(self.master, self, "Add Department")

    def edit_department(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a department to edit.")
            return

        item = self.tree.item(selected[0])
        dep_id, department_name, manager = item['values']
        DepartmentForm(self.master, self, "Edit Department", dep_id, department_name, manager)

    def delete_department(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a department to delete.")
            return

        item = self.tree.item(selected[0])
        dep_id = item['values'][0]

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this department?"):
            if delete_department(dep_id):
                messagebox.showinfo("Success", "Department deleted successfully.")
                self.load_departments()
            else:
                messagebox.showerror("Error", "Failed to delete department.")
