from ttkbootstrap import Frame, Label, Entry, Combobox, Button, Scrollbar, Treeview
from ttkbootstrap.constants import *
from datetime import datetime

from ..config import (
    add_attendance,
    get_all_attendance,
    delete_attendance_by_id,
    get_all_employee_names
)


class AttendanceView(Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self.master = master
        self.build_ui()
        self.populate_employee_names()
        self.load_attendance()

    def build_ui(self):
        Label(self, text="Attendance Tracking", font=("Segoe UI", 20, "bold"))\
            .pack(anchor="w", pady=(0, 20))

        # === Form Input ===
        form = Frame(self)
        form.pack(fill="x", pady=(0, 10))

        Label(form, text="Employee Name").grid(row=0, column=0, sticky="w", padx=5)
        self.name_combo = Combobox(form, state="readonly")
        self.name_combo.grid(row=0, column=1, padx=5)

        Label(form, text="Status").grid(row=0, column=2, sticky="w", padx=5)
        self.status_combo = Combobox(form, values=["Present", "Absent", "On Leave"], state="readonly")
        self.status_combo.grid(row=0, column=3, padx=5)

        Label(form, text="Check-in").grid(row=1, column=0, sticky="w", padx=5)
        self.checkin_entry = Entry(form)
        self.checkin_entry.grid(row=1, column=1, padx=5)

        Label(form, text="Check-out").grid(row=1, column=2, sticky="w", padx=5)
        self.checkout_entry = Entry(form)
        self.checkout_entry.grid(row=1, column=3, padx=5)

        Label(form, text="Notes").grid(row=2, column=0, sticky="w", padx=5)
        self.notes_entry = Entry(form, width=80)
        self.notes_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        # === Buttons ===
        btn_frame = Frame(self)
        btn_frame.pack(fill="x", pady=10)

        Button(btn_frame, text="Add Attendance", bootstyle="primary", command=self.add_attendance)\
            .pack(side="left", padx=5)

        Button(btn_frame, text="Edit Selected", bootstyle="warning", command=self.edit_selected)\
            .pack(side="left", padx=5)

        Button(btn_frame, text="Delete Selected", bootstyle="danger", command=self.delete_selected)\
            .pack(side="left", padx=5)

        # === Table ===
        table_frame = Frame(self)
        table_frame.pack(fill="both", expand=True)

        vsb = Scrollbar(table_frame, orient="vertical")
        vsb.pack(side="right", fill="y")

        hsb = Scrollbar(table_frame, orient="horizontal")
        hsb.pack(side="bottom", fill="x")

        self.tree = Treeview(
            table_frame,
            columns=("Date", "Employee Name", "Status", "Check-in", "Check-out", "Notes"),
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=15
        )
        self.tree.pack(fill="both", expand=True)
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)

        self.tree.column("Notes", width=200, anchor="w")

        self.tree.tag_configure('oddrow', background='#d0ebff')
        self.tree.tag_configure('evenrow', background='white')

    def populate_employee_names(self):
        names = get_all_employee_names()
        self.name_combo['values'] = names

    def load_attendance(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        records = get_all_attendance()
        for index, record in enumerate(records):
            tag = 'oddrow' if index % 2 == 0 else 'evenrow'
            self.tree.insert("", "end", values=(
                record[6],  # date
                record[1],  # employee_name
                record[2],  # status
                record[3],  # checkin
                record[4],  # checkout
                record[5],  # notes
            ), tags=(tag,))

    def add_attendance(self):
        name = self.name_combo.get()
        status = self.status_combo.get()
        checkin = self.checkin_entry.get()
        checkout = self.checkout_entry.get()
        notes = self.notes_entry.get()
        date = datetime.now().strftime("%Y-%m-%d")

        if name and status:
            success = add_attendance(name, status, checkin, checkout, notes, date)
            if success:
                self.load_attendance()
                self.clear_form()

    def edit_selected(self):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])["values"]
            self.name_combo.set(values[1])
            self.status_combo.set(values[2])
            self.checkin_entry.delete(0, "end")
            self.checkin_entry.insert(0, values[3])
            self.checkout_entry.delete(0, "end")
            self.checkout_entry.insert(0, values[4])
            self.notes_entry.delete(0, "end")
            self.notes_entry.insert(0, values[5])
            self.tree.delete(selected[0])

    def delete_selected(self):
        selected = self.tree.selection()
        for item in selected:
            self.tree.delete(item)

    def clear_form(self):
        self.name_combo.set("")
        self.status_combo.set("")
        self.checkin_entry.delete(0, "end")
        self.checkout_entry.delete(0, "end")
        self.notes_entry.delete(0, "end")
