from tkinter import filedialog, messagebox
import ttkbootstrap as tb


from app.config import get_payroll_summary_by_period
from app.utils.report_exporter import export_to_excel, export_to_csv


class ReportView(tb.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self.master = master
        self.build_ui()

    def build_ui(self):
        tb.Label(self, text="Payroll Report", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 10))

        # Filter section
        filter_frame = tb.Frame(self)
        filter_frame.pack(fill="x", pady=(0, 10))

        tb.Label(filter_frame, text="Payroll Period (e.g. 2025-06):").pack(side="left")
        self.period_var = tb.StringVar()
        self.entry_period = tb.Entry(filter_frame, textvariable=self.period_var)
        self.entry_period.pack(side="left", padx=5)
        tb.Button(filter_frame, text="Generate", bootstyle="primary", command=self.generate_report).pack(side="left", padx=5)

        # Export buttons
        export_frame = tb.Frame(self)
        export_frame.pack(fill="x", pady=(10, 20))
        tb.Button(export_frame, text="Export to CSV", bootstyle="info", command=self.export_csv).pack(side="left", padx=5)
        tb.Button(export_frame, text="Export to Excel", bootstyle="info", command=self.export_excel).pack(side="left", padx=5)

        # Table section
        table_frame = tb.Frame(self)
        table_frame.pack(fill="both", expand=True)

        self.tree = tb.Treeview(
            table_frame,
            columns=("Employee Name", "Base Salary", "Bonus", "Deductions", "Net Pay"),
            show="headings",
            height=15,
            style="info.Treeview"
        )
        self.tree.pack(fill="both", expand=True)

        self.tree.heading("Employee Name", text="Employee Name")
        self.tree.heading("Base Salary", text="Base Salary")
        self.tree.heading("Bonus", text="Bonus")
        self.tree.heading("Deductions", text="Deductions")
        self.tree.heading("Net Pay", text="Net Pay")

        for col in ("Base Salary", "Bonus", "Deductions", "Net Pay"):
            self.tree.column(col, anchor="e", width=100)
        self.tree.column("Employee Name", anchor="w", width=180)

    def export_csv(self):
        # Open file dialog to select location and filename
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if filename:
            export_to_csv(self.tree, filename)

    def export_excel(self):
        # Open file dialog to select location and filename
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if filename:
            export_to_excel(self.tree, filename)

    def generate_report(self):
        period = self.period_var.get().strip()
        if not period:
            messagebox.showwarning("Input Error", "Please enter a payroll period (e.g. 2025-06)")
            return

        # Generate the report using ReportController
        # Use your `ReportController` class to get results and update table
        results = get_payroll_summary_by_period(period)
        self.update_report_table(results)

    def update_report_table(self, results):
        # Update the table with the fetched results
        self.tree.delete(*self.tree.get_children())
        for row in results:
            name, base, bonus, deductions, net = row
            self.tree.insert("", "end", values=(
                name,
                f"${base:,.2f}",
                f"${bonus:,.2f}",
                f"${deductions:,.2f}",
                f"${net:,.2f}",
            ))
