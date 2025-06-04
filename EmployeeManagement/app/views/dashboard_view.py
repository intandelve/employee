import os
from PIL import Image, ImageTk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

from app.views.Overview import OverviewPage
# Import all views
from app.views.employee import EmployeeView
from app.views.department import DepartmentView
from app.views.attendance import AttendanceView
from app.views.payroll import PayrollView
from app.views.report import ReportView
from app.views.settings import SettingsView


class DashboardView(tb.Frame):
    def __init__(self, master, username=None):  # username jadi opsional
        super().__init__(master)
        self.master = master
        self.username = username  # simpan username, walaupun bisa None
        self.style = tb.Style()
        self.default_theme = self.style.theme.name
        self.pack(fill="both", expand=True)
        self.views = {}
        self.build_ui()


    def build_ui(self):
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.style.configure("Sidebar.TFrame", background="#7b5a84")
        self.style.configure("Sidebar.TButton",
                             background="#b79cb9",
                             foreground="white",
                             font=("Segoe UI", 12),
                             padding=10,
                             borderwidth=0)
        self.style.map("Sidebar.TButton",
                       background=[("active", "#9b7dbd"), ("pressed", "#7a699e")],
                       foreground=[("active", "white"), ("pressed", "white")])

        # Sidebar
        sidebar = tb.Frame(self, width=360, style="Sidebar.TFrame")
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        sidebar.columnconfigure(0, weight=1)

        try:
            image_path = os.path.join("resources", "icon.jpg")
            image = Image.open(image_path).resize((120, 120))
            self.logo_image = ImageTk.PhotoImage(image)
            logo_label = tb.Label(sidebar, image=self.logo_image, background="#7b5a84")
            logo_label.grid(row=0, column=0, pady=(30, 5))
        except Exception as e:
            print(f"Logo load error: {e}")

        title = tb.Label(sidebar, text="Dashboard",
                         font=("Segoe UI", 20, "bold"),
                         background="#7b5a84",
                         foreground="white")
        title.grid(row=1, column=0, pady=(5, 30))

        self.features = [
            "Dashboard Overview",
            "Employee Data",
            "Departments",
            "Attendance",
            "Payroll",
            "Report",
            "Setting",
        ]

        for index, feature in enumerate(self.features, start=2):
            btn = tb.Button(
                sidebar,
                text=feature,
                style="Sidebar.TButton",
                command=lambda f=feature: self.show_feature(f)
            )
            btn.grid(row=index, column=0, padx=20, pady=5, sticky="ew")

        # Main content panel
        self.content = tb.Frame(self, padding=30)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.columnconfigure(0, weight=1)

        self.show_dashboard_home()  # Initial welcome screen

    def show_dashboard_home(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        tb.Label(
            self.content,
            text="Welcome to the Employee Management Dashboard",
            font=("Segoe UI", 18, "bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 20))

        tb.Label(
            self.content,
            text="Please select a menu from the left to begin.",
            font=("Segoe UI", 12)
        ).grid(row=1, column=0, sticky="w")

    def show_feature(self, feature_name):
        for widget in self.content.winfo_children():
            widget.destroy()

        if feature_name == "Dashboard Overview":
            self.load_view("overview", lambda parent: OverviewPage(parent, self.style))
        elif feature_name == "Employee Data":
            self.load_view("employee", EmployeeView)
        elif feature_name == "Departments":
            self.load_view("department", DepartmentView)
        elif feature_name == "Attendance":
            self.load_view("attendance", AttendanceView)
        elif feature_name == "Payroll":
            self.load_view("payroll", PayrollView)
        elif feature_name == "Report":
            self.load_view("report", ReportView)
        elif feature_name == "Setting":
            self.load_view("settings", lambda parent: SettingsView(parent, self.style, self.default_theme, self.username, lambda: self.master.show_login()))

        else:
            tb.Label(
                self.content,
                text=feature_name,
                font=("Segoe UI", 18, "bold")
            ).grid(row=0, column=0, sticky="w", pady=(0, 20))
            tb.Label(
                self.content,
                text=f"{feature_name} UI will go here soon.",
                font=("Segoe UI", 12)
            ).grid(row=1, column=0, sticky="w")

    def load_view(self, key, view_class):
        if key in self.views:
            self.views[key].destroy()

        view = view_class(self.content) if callable(view_class) else view_class(self.content)

        view.pack(fill="both", expand=True)
        self.views[key] = view
