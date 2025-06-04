
from app.config.database import get_payroll_summary_by_period
from app.views.report import ReportView


class ReportController:
    def __init__(self, master):
        self.master = master
        self.report_view = ReportView(master)

    def generate_report(self, period):
        # Mengambil data laporan dari database
        results = get_payroll_summary_by_period(period)
        self.report_view.update_report_table(results)
