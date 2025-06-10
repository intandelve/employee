import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from ttkbootstrap.tooltip import ToolTip
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

from app.config import create_connection


class OverviewPage(ttk.Frame):
    def __init__(self, parent, style: Style, show_feature_callback):
        super().__init__(parent)
        self.style = style
        self.show_feature_callback = show_feature_callback
        self.configure(padding=15, style="whiteframe.TFrame")
        self.build_ui()

    def build_ui(self):
        self.columnconfigure(0, weight=1)

        # === Header ===
        header = ttk.Label(
            self,
            text="📊 Dashboard Overview",
            font=("Segoe UI", 22, "bold"),
            foreground="#5e548e",
            anchor="w",
        )
        header.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        # Underline bar below header
        underline = ttk.Frame(self, height=3, style="primary.Horizontal.TSeparator")
        underline.grid(row=1, column=0, sticky="ew", pady=(0, 15))

        # === Statistic Cards ===
        card_frame = ttk.Frame(self, style="whiteframe.TFrame")
        card_frame.grid(row=2, column=0, sticky="ew")
        for i in range(4):
            card_frame.columnconfigure(i, weight=1)

        stats = [
            ("Total Employees", self.get_employee_count(), "👥", "Total number of employees", "Employee Data"),
            ("Attendance Today", self.get_attendance_count(), "📅", "Number of employees present today", "Attendance"),
            ("Total Payrolls", self.get_payroll_count(), "💰", "Payroll records processed", "Payroll"),
            ("Departments", self.get_department_count(), "🏢", "Active departments in company", "Departments"),
        ]

        for idx, (title, value, icon, tooltip_text, feature_name) in enumerate(stats):
            self.create_card(card_frame, title, value, icon, tooltip_text, column=idx, feature_name=feature_name)

        # === Charts Section ===
        chart_container = ttk.Frame(self, style="whiteframe.TFrame")
        chart_container.grid(row=3, column=0, sticky="nsew", pady=(20, 5))
        chart_container.columnconfigure(0, weight=1)

        attendance_frame = ttk.LabelFrame(
            chart_container, text="📈 Attendance Summary (Last 7 Days)", padding=(10, 10)
        )
        attendance_frame.grid(row=0, column=0, sticky="nsew")
        self.build_attendance_chart(attendance_frame)

        # === Footer / Notes ===
        footer = ttk.Label(
            self,
            text="* Data updates every time this page is opened",
            font=("Segoe UI", 9, "italic"),
            foreground="#6c757d",
            anchor="w",
        )
        footer.grid(row=4, column=0, sticky="w", pady=(15, 0))

    def create_card(self, parent, title, value, icon_emoji, tooltip_text, column, feature_name):
        # Card container with padding and style
        card = ttk.Frame(parent, style="secondary.TFrame", padding=15)
        card.grid(row=0, column=column, padx=10, pady=8, sticky="nsew")

        # Add rounded corners and shadow by wrapping card into a Canvas (optional, advanced)

        # Icon
        icon_label = ttk.Label(card, text=icon_emoji, font=("Segoe UI Emoji", 30))
        icon_label.pack(anchor="w", pady=(0, 8))

        # Title
        title_label = ttk.Label(card, text=title, font=("Segoe UI", 11, "bold"), foreground="#6c757d")
        title_label.pack(anchor="w")

        # Value
        value_label = ttk.Label(card, text=str(value), font=("Segoe UI", 28, "bold"), foreground="#343a40")
        value_label.pack(anchor="w", pady=(4, 0))

        # Tooltip on the entire card
        ToolTip(card, text=tooltip_text, delay=0.5)

        # Hover effect (background change)
        def on_enter(e):
            card.configure(style="info.TFrame")
            if hasattr(self, 'show_feature_callback') and self.show_feature_callback and feature_name:
                card.config(cursor="hand2")

        def on_leave(e):
            card.configure(style="secondary.TFrame")
            if hasattr(self, 'show_feature_callback') and self.show_feature_callback and feature_name:
                card.config(cursor="")

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        if self.show_feature_callback and feature_name:
            card.bind("<Button-1>", lambda event, fn=feature_name: self.show_feature_callback(fn))

    def build_attendance_chart(self, parent):
        days, counts = self.get_attendance_last_7_days()

        fig, ax = plt.subplots(figsize=(7, 4), dpi=100)
        bars = ax.bar(days, counts, color="#b79cb9", edgecolor="#5e548e", linewidth=1.5)

        ax.set_ylabel("Count", fontsize=11, fontweight="bold")
        ax.set_xlabel("Date", fontsize=11, fontweight="bold")
        ax.set_title("Employee Attendance", fontsize=14, fontweight="bold", color="#5e548e")
        ax.set_ylim(0, max(counts + [1]) + 3)
        ax.grid(axis="y", linestyle="--", alpha=0.5)

        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f"{height}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5),  # offset
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=9,
                color="#5e548e",
                fontweight="bold",
            )

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # ==== Database Queries ====

    def fetch_count(self, query):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count

    def get_employee_count(self):
        return self.fetch_count("SELECT COUNT(*) FROM employees")

    def get_attendance_count(self):
        return self.fetch_count("SELECT COUNT(*) FROM attendance WHERE DATE(date) = CURDATE()")

    def get_payroll_count(self):
        return self.fetch_count("SELECT COUNT(*) FROM payroll")

    def get_department_count(self):
        return self.fetch_count("SELECT COUNT(*) FROM departments")

    def get_attendance_last_7_days(self):
        conn = create_connection()
        cursor = conn.cursor()

        base = datetime.today()
        date_list = [(base - timedelta(days=x)).date() for x in range(6, -1, -1)]
        counts_dict = {d: 0 for d in date_list}

        cursor.execute(
            """
            SELECT DATE(date), COUNT(*) 
            FROM attendance 
            WHERE date >= CURDATE() - INTERVAL 6 DAY 
            GROUP BY DATE(date)
            ORDER BY DATE(date)
            """
        )
        rows = cursor.fetchall()

        for row in rows:
            counts_dict[row[0]] = row[1]

        cursor.close()
        conn.close()

        counts = [counts_dict[d] for d in date_list]
        date_str_list = [d.strftime("%m-%d") for d in date_list]
        return date_str_list, counts
