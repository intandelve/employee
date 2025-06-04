import ttkbootstrap as tb
from ttkbootstrap.constants import *

from app.config import register_user


class RegisterView(tb.Frame):
    def __init__(self, master, switch_to_login):
        super().__init__(master, padding=40)
        self.master = master
        self.switch_to_login = switch_to_login
        self.pack(fill="both", expand=True)
        self.build_ui()

    def build_ui(self):
        self.columnconfigure(0, weight=1)

        tb.Label(self, text="Register", font=("Segoe UI", 28, "bold")).grid(row=0, column=0, pady=(0, 30))

        self.email = tb.Entry(self, bootstyle="info")
        self._set_placeholder(self.email, "Email")
        self.email.grid(row=1, column=0, sticky="ew", pady=8)

        self.username = tb.Entry(self, bootstyle="info")
        self._set_placeholder(self.username, "Username")
        self.username.grid(row=2, column=0, sticky="ew", pady=8)

        self.password = tb.Entry(self, show="*", bootstyle="info")
        self._set_placeholder(self.password, "Password", is_password=True)
        self.password.grid(row=3, column=0, sticky="ew", pady=8)

        self.confirm_password = tb.Entry(self, show="*", bootstyle="info")
        self._set_placeholder(self.confirm_password, "Confirm Password", is_password=True)
        self.confirm_password.grid(row=4, column=0, sticky="ew", pady=8)

        self.feedback = tb.Label(self, text="", foreground="red")
        self.feedback.grid(row=5, column=0, pady=(5, 15))

        tb.Button(self, text="Register", bootstyle="success", command=self.register_user)\
            .grid(row=6, column=0, sticky="ew", pady=(0, 10))

        tb.Button(self, text="Back to Login", bootstyle="secondary", command=self.switch_to_login)\
            .grid(row=7, column=0, sticky="ew")

    def _set_placeholder(self, entry, placeholder, is_password=False):
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, 'end')
                if is_password:
                    entry.config(show="*")
                entry.config(foreground="black")

        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder)
                if is_password:
                    entry.config(show="")
                entry.config(foreground="gray")

        entry.insert(0, placeholder)
        entry.config(foreground="gray")
        if is_password:
            entry.config(show="")
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def register_user(self):
        email = self.email.get().strip()
        username = self.username.get().strip()
        password = self.password.get()
        confirm = self.confirm_password.get()

        if email == "" or email == "Email":
            self.feedback.config(text="Please enter your email.")
            return
        if "@" not in email or "." not in email:
            self.feedback.config(text="Invalid email format.")
            return

        if username == "" or username == "Username":
            self.feedback.config(text="Please enter a username.")
            return

        if password == "" or password == "Password":
            self.feedback.config(text="Please enter a password.")
            return

        if password != confirm:
            self.feedback.config(text="Passwords do not match.")
            return

        success, message = register_user(email, username, password)
        if success:
            self.feedback.config(text=message, foreground="green")
            # Optionally auto switch:
            # self.switch_to_login()
        else:
            self.feedback.config(text=message, foreground="red")
