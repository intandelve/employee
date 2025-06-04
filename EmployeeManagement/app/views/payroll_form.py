import ttkbootstrap as tb
from tkinter import messagebox

from app.config.database import get_all_employees, insert_payroll, update_payroll

class PayrollForm(tb.Toplevel):
    def __init__(self, master, refresh_callback, payroll=None):
        super().__init__(master)
        self.title("Add Payroll" if payroll is None else "Edit Payroll")
        self.geometry("700x700")
        self.resizable(False, False)

        self.refresh_callback = refresh_callback
        self.payroll = payroll
        self.employees = get_all_employees()

        self.configure(padx=20, pady=20)
        self.build_ui()

        if self.payroll:
            self.fill_form()

        self.transient(master)
        self.grab_set()
        self.focus()

    def build_ui(self):
        label_font = ("Segoe UI", 10)
        entry_padding = {"padx": 0, "pady": (5, 15)}

        title_text = "Edit Payroll" if self.payroll else "Add New Payroll"
        tb.Label(self, text=title_text, font=("Segoe UI", 16, "bold")).pack(pady=(0, 20))

        tb.Label(self, text="Payroll Period (e.g. 2025-06)", font=label_font).pack(anchor="w")
        self.entry_period = tb.Entry(self)
        self.entry_period.pack(fill="x", **entry_padding)

        tb.Label(self, text="Select Employee", font=label_font).pack(anchor="w")
        self.employee_var = tb.StringVar()
        self.employee_combo = tb.Combobox(
            self,
            values=[e[1] for e in self.employees],
            textvariable=self.employee_var,
            state="readonly"
        )
        self.employee_combo.pack(fill="x", **entry_padding)
        self.employee_combo.bind("<<ComboboxSelected>>", self.on_employee_selected)

        tb.Label(self, text="Base Salary", font=label_font).pack(anchor="w")
        self.entry_base_salary = tb.Entry(self)
        self.entry_base_salary.pack(fill="x", **entry_padding)

        tb.Label(self, text="Bonus", font=label_font).pack(anchor="w")
        self.entry_bonus = tb.Entry(self)
        self.entry_bonus.insert(0, "0")
        self.entry_bonus.pack(fill="x", **entry_padding)

        tb.Label(self, text="Deductions", font=label_font).pack(anchor="w")
        self.entry_deductions = tb.Entry(self)
        self.entry_deductions.insert(0, "0")
        self.entry_deductions.pack(fill="x", **entry_padding)

        tb.Label(self, text="Status", font=label_font).pack(anchor="w")
        self.status_var = tb.StringVar(value="Pending")
        self.status_combo = tb.Combobox(self, values=["Paid", "Pending"], textvariable=self.status_var, state="readonly")
        self.status_combo.pack(fill="x", **entry_padding)

        tb.Button(self, text="Save Payroll", bootstyle="success", command=self.submit).pack(pady=(10, 0), fill="x")

    def on_employee_selected(self, event):
        selected_name = self.employee_var.get()
        # Employee tuple index 5 (6th column) = basic_salary according to your info
        employee = next((e for e in self.employees if e[1] == selected_name), None)
        if employee:
            base_salary = employee[5]  # index 5 for basic_salary
            self.entry_base_salary.delete(0, "end")
            self.entry_base_salary.insert(0, str(base_salary))

    def fill_form(self):
        _id, employee_id, period, base_salary, bonus, deductions, net_pay, status = self.payroll
        self.entry_period.insert(0, period)
        employee_name = next((e[1] for e in self.employees if e[0] == employee_id), "")
        self.employee_var.set(employee_name)
        self.entry_base_salary.insert(0, str(base_salary))
        self.entry_bonus.insert(0, str(bonus))
        self.entry_deductions.insert(0, str(deductions))
        self.status_var.set(status)

    def submit(self):
        period = self.entry_period.get().strip()
        employee_name = self.employee_var.get().strip()
        base_salary = self.entry_base_salary.get().strip()
        bonus = self.entry_bonus.get().strip()
        deductions = self.entry_deductions.get().strip()
        status = self.status_var.get().strip()

        if not period or not employee_name or not base_salary:
            messagebox.showerror("Error", "Period, Employee, and Base Salary are required!")
            return

        try:
            base_salary = float(base_salary)
            bonus = float(bonus) if bonus else 0.0
            deductions = float(deductions) if deductions else 0.0
        except ValueError:
            messagebox.showerror("Error", "Salary, Bonus, and Deductions must be numbers!")
            return

        net_pay = base_salary + bonus - deductions

        employee_id = next((e[0] for e in self.employees if e[1] == employee_name), None)
        if employee_id is None:
            messagebox.showerror("Error", "Selected employee not found!")
            return

        try:
            if self.payroll:
                payroll_id = self.payroll[0]
                success = update_payroll(payroll_id, employee_id, period, base_salary, bonus, deductions, net_pay, status)
                if success:
                    messagebox.showinfo("Success", "Payroll updated successfully")
                    self.refresh_callback()
                    self.destroy()
                else:
                    messagebox.showerror("Error", "Failed to update payroll")
            else:
                insert_payroll(employee_id, period, base_salary, bonus, deductions, net_pay, status)
                messagebox.showinfo("Success", "Payroll saved successfully.")
                self.refresh_callback()
                self.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save payroll:\n{e}")
