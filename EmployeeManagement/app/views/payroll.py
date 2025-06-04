from tkinter import messagebox
import ttkbootstrap as tb

from app.config import get_all_payroll, create_connection, get_payroll_by_id
from app.views.payroll_form import PayrollForm

class PayrollView(tb.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self.master = master
        self.payroll_data = {}  # Cache payroll rows by ID
        self.build_ui()

    def build_ui(self):
        title = tb.Label(self, text="Payroll Management", font=("Segoe UI", 16, "bold"))
        title.pack(anchor="w", pady=(0, 10))

        table_frame = tb.Frame(self)
        table_frame.pack(fill="both", expand=True)

        vsb = tb.Scrollbar(table_frame, orient="vertical")
        vsb.pack(side="right", fill="y")

        self.tree = tb.Treeview(
            table_frame,
            columns=("Period", "Employee Name", "Base Salary", "Bonus", "Deductions", "Net Pay", "Status"),
            show="headings",
            yscrollcommand=vsb.set,
            height=15,
            style="info.Treeview"
        )
        self.tree.pack(fill="both", expand=True)
        vsb.config(command=self.tree.yview)

        # Setup headings and column widths
        self.tree.heading("Period", text="Period")
        self.tree.column("Period", width=100, anchor="center")

        self.tree.heading("Employee Name", text="Employee Name")
        self.tree.column("Employee Name", width=180, anchor="w")

        self.tree.heading("Base Salary", text="Base Salary")
        self.tree.column("Base Salary", width=100, anchor="e")

        self.tree.heading("Bonus", text="Bonus")
        self.tree.column("Bonus", width=80, anchor="e")

        self.tree.heading("Deductions", text="Deductions")
        self.tree.column("Deductions", width=100, anchor="e")

        self.tree.heading("Net Pay", text="Net Pay")
        self.tree.column("Net Pay", width=100, anchor="e")

        self.tree.heading("Status", text="Status")
        self.tree.column("Status", width=100, anchor="center")

        # Configure row tags for colors
        self.tree.tag_configure('oddrow', background='#f0e9f5')  # light purple
        self.tree.tag_configure('evenrow', background='white')

        self.refresh_table()

        btn_frame = tb.Frame(self)
        btn_frame.pack(fill="x", pady=(10, 0))

        btn_add = tb.Button(btn_frame, text="Add Payroll", bootstyle="primary", command=self.on_add_payroll)
        btn_add.pack(side="left", padx=5)

        btn_edit = tb.Button(btn_frame, text="Edit Selected", bootstyle="warning", command=self.on_edit_payroll)
        btn_edit.pack(side="left", padx=5)

        btn_delete = tb.Button(btn_frame, text="Delete Selected", bootstyle="danger", command=self.on_delete_payroll)
        btn_delete.pack(side="left", padx=5)

    def refresh_table(self):
        # Clear existing rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        rows = get_all_payroll()
        self.payroll_data.clear()

        for i, row in enumerate(rows):
            # row: id, employee name, period, base_salary, bonus, deductions, net_pay, status
            self.payroll_data[row[0]] = row

            try:
                net_pay_val = float(row[6]) if row[6] else 0.0
            except (ValueError, TypeError):
                net_pay_val = 0.0

            net_pay_str = f"${net_pay_val:,.2f}"

            values = (
                row[1],  # Period
                row[2],  # Employee Name
                f"${float(row[3]):,.2f}",  # Base Salary
                f"${float(row[4]):,.2f}",  # Bonus
                f"${float(row[5]):,.2f}",  # Deductions
                net_pay_str,
                row[7],  # Status
            )

            tag = 'evenrow' if i % 2 == 0 else 'oddrow'

            # Set the DB payroll ID as Treeview item id (iid)
            self.tree.insert("", "end", iid=str(row[0]), values=values, tags=(tag,))

    def on_add_payroll(self):
        PayrollForm(self.master, self.refresh_table)

    def on_edit_payroll(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a payroll to edit.")
            return

        payroll_id = int(selected[0])
        payroll = get_payroll_by_id(payroll_id)
        if not payroll:
            messagebox.showerror("Error", "Payroll data not found for editing.")
            return

        PayrollForm(self.master, self.refresh_table, payroll=payroll)

    def on_delete_payroll(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a payroll to delete")
            return
        payroll_id = int(selected[0])

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this payroll?"):
            connection = create_connection()
            if not connection:
                messagebox.showerror("Error", "Failed to connect to database")
                return
            try:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM payroll WHERE id = %s", (payroll_id,))
                connection.commit()
                messagebox.showinfo("Success", "Payroll deleted successfully")
                self.refresh_table()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete payroll:\n{e}")
            finally:
                cursor.close()
                connection.close()
