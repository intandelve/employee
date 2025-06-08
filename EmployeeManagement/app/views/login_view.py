import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import os

from app.config import login_user


class LoginView(tb.Frame):
    def __init__(self, master, switch_to_register, switch_to_dashboard):
        super().__init__(master)
        self.master = master
        self.switch_to_register = switch_to_register
        self.switch_to_dashboard = switch_to_dashboard
        self.pack(fill="both", expand=True)
        self.build_ui()

    def build_ui(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)

        # LEFT PANEL
        left_panel = tb.Frame(self, width=300)
        left_panel.grid(row=0, column=0, sticky="nsew")
        left_panel.configure(style="Left.TFrame")
        left_panel.grid_propagate(False)
        left_panel.columnconfigure(0, weight=1)
        left_panel.rowconfigure(2, weight=1)

        try:
            image_path = os.path.join("resources", "icon.jpg")
            image = Image.open(image_path).resize((400, 400))
            self.logo_image = ImageTk.PhotoImage(image)
            logo_label = tb.Label(left_panel, image=self.logo_image, background="#b79cb9")
            logo_label.grid(row=0, column=0, pady=(70, 20))
        except Exception as e:
            print(f"Logo load error: {e}")

        welcome_label = tb.Label(
            left_panel,
            text="Welcome!",
            font=("Segoe UI", 50, "bold"),
            background="#b79cb9",
            foreground="white"
        )
        welcome_label.grid(row=1, column=0, pady=20)

        # RIGHT PANEL
        right_panel = tb.Frame(self)
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(0, weight=1)

        center_wrapper = tb.Frame(right_panel)
        center_wrapper.grid(row=0, column=0)
        center_wrapper.columnconfigure(0, weight=1)
        center_wrapper.rowconfigure(0, weight=1)

        form_container = tb.Frame(center_wrapper, padding=80)
        form_container.grid(row=0, column=0)
        form_container.columnconfigure(0, weight=1)

        tb.Label(form_container, text="Login", font=("Segoe UI", 36, "bold")).grid(
            row=0, column=0, pady=(0, 40)
        )

        self.email_entry = tb.Entry(form_container, bootstyle="info", width=40)
        self._set_placeholder(self.email_entry, "Email")
        self.email_entry.grid(row=1, column=0, pady=15, ipady=10, sticky="ew")

        self.password_entry = tb.Entry(form_container, bootstyle="info", width=40)
        self._set_placeholder(self.password_entry, "Password", is_password=True)
        self.password_entry.grid(row=2, column=0, pady=15, ipady=10, sticky="ew")

        self.feedback = tb.Label(form_container, text="", foreground="red")
        self.feedback.grid(row=3, column=0, pady=(5, 15))

        tb.Button(form_container, text="Login", bootstyle="success", command=self.login).grid(
            row=4, column=0, pady=(10, 15), ipady=8, sticky="ew"
        )
        tb.Button(form_container, text="Register", bootstyle="secondary", command=self.register).grid(
            row=5, column=0, ipady=8, sticky="ew"
        )

        style = tb.Style()
        style.configure("Left.TFrame", background="#b79cb9")

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

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        if email == "" or email == "Email":
            self.feedback.config(text="Please enter your email")
            return
        if password == "" or password == "Password": # Assuming "Password" is placeholder
            self.feedback.config(text="Please enter your password")
            return

        success, result_data = login_user(email, password) # result_data is dict on success
        if success:
            username = result_data["username"] # Extract username
            # User_id = result_data["id"] # If needed later
            self.feedback.config(text="Login successful!", foreground="green") # Generic success
            self.switch_to_dashboard(username) # Pass username
        else:
            # result_data is an error message string here
            self.feedback.config(text=result_data, foreground="red")

    def register(self):
        self.switch_to_register()
