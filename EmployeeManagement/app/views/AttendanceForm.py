import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
from ttkbootstrap.dialogs import DatePickerDialog
from datetime import datetime

from app.config import get_all_employees, add_attendance


class AttendanceForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Attendance")
        self.geometry("400x450")
        self.resizable(False, False)

        self.style = Style("flatly")

        # Employee dropdown
        ttk.Label(self, text="Employee").pack(pady=5)
        self.employee_cb = ttk.Combobox(self, state="readonly")
        self.employee_cb['values'] = [emp[1] for emp in get_all_employees()]  # emp[1] is name
        self.employee_cb.pack(pady=5, fill='x', padx=20)

        # Status
        ttk.Label(self, text="Status").pack(pady=5)
        self.status_cb = ttk.Combobox(self, state="readonly")
        self.status_cb['values'] = ["Present", "Absent", "Sick", "Leave"]
        self.status_cb.current(0)
        self.status_cb.pack(pady=5, fill='x', padx=20)

        # Check-in
        ttk.Label(self, text="Check-in Time (HH:MM)").pack(pady=5)
        self.checkin_entry = ttk.Entry(self)
        self.checkin_entry.insert(0, datetime.now().strftime("%H:%M"))
        self.checkin_entry.pack(pady=5, fill='x', padx=20)

        # Check-out
        ttk.Label(self, text="Check-out Time (HH:MM)").pack(pady=5)
        self.checkout_entry = ttk.Entry(self)
        self.checkout_entry.insert(0, "")
        self.checkout_entry.pack(pady=5, fill='x', padx=20)

        # Notes
        ttk.Label(self, text="Notes").pack(pady=5)
        self.notes_entry = ttk.Entry(self)
        self.notes_entry.pack(pady=5, fill='x', padx=20)

        # Date
        ttk.Label(self, text="Date").pack(pady=5)
        self.date_var = tk.StringVar(value=datetime.today().strftime("%Y-%m-%d"))
        self.date_entry = ttk.Entry(self, textvariable=self.date_var, state="readonly")
        self.date_entry.pack(pady=5, fill='x', padx=20)

        date_button = ttk.Button(self, text="Pick Date", command=self.pick_date)
        date_button.pack(pady=5)

        # Submit
        submit_btn = ttk.Button(self, text="Submit", command=self.submit_form)
        submit_btn.pack(pady=15)

    def pick_date(self):
        result = DatePickerDialog(self).show()
        if result:
            self.date_var.set(result.strftime("%Y-%m-%d"))

    def submit_form(self):
        name = self.employee_cb.get()
        status = self.status_cb.get()
        checkin = self.checkin_entry.get()
        checkout = self.checkout_entry.get()
        notes = self.notes_entry.get()
        date = self.date_var.get()

        if not all([name, status, checkin, date]):
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        success = add_attendance(name, status, checkin, checkout, notes, date)
        if success:
            messagebox.showinfo("Success", "Attendance added successfully.")
            self.destroy()
        else:
            messagebox.showerror("Error", "Failed to add attendance.")
