import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
import hashlib
from app.config import create_connection  # your DB connection helper


class SettingsView(tb.Frame):
    def __init__(self, master, style, default_theme, username, on_logout):
        super().__init__(master, padding=10)
        self.master = master
        self.style = style
        self.default_theme = default_theme
        self.username = username
        self.on_logout = on_logout  # callback to logout
        self.user_data = {}

        self.load_user_data()
        self.build_ui()

    def load_user_data(self):
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM users WHERE username = %s", (self.username,))
            row = cursor.fetchone()
            if row:
                self.user_data["email"] = row[0]
            else:
                print(f"Error: User not found in database for username: {self.username}") # Changed
                self.user_data["email"] = ""
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Database Error: Failed to load user data for {self.username}. Error: {e}") # Changed
            self.user_data["email"] = ""

    def build_ui(self):
        tb.Label(self, text="Settings", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 10))

        # Theme Settings
        theme_frame = tb.Labelframe(self, text="Theme Settings", padding=10)
        theme_frame.pack(fill="x", pady=10)

        tb.Label(theme_frame, text="Choose Theme:").pack(side="left", padx=(0, 10))

        self.theme_var = tb.StringVar(value=self.style.theme.name)
        theme_combo = tb.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=self.style.theme_names(),
            state="readonly",
            width=20
        )
        theme_combo.pack(side="left", padx=5)

        tb.Button(theme_frame, text="Apply", bootstyle="primary", command=self.change_theme).pack(side="left", padx=5)
        tb.Button(theme_frame, text="Reset to Default", bootstyle="secondary", command=self.reset_theme).pack(side="left", padx=5)

        # Profile Management
        profile_frame = tb.Labelframe(self, text="User Profile Management", padding=10)
        profile_frame.pack(fill="both", expand=True, pady=10)

        tb.Label(profile_frame, text="Email:").grid(row=0, column=0, sticky="w", pady=5)
        self.email_var = tb.StringVar(value=self.user_data.get("email", ""))
        tb.Entry(profile_frame, textvariable=self.email_var, width=40).grid(row=0, column=1, pady=5)

        tb.Label(profile_frame, text="New Password:").grid(row=1, column=0, sticky="w", pady=5)
        self.password_var = tb.StringVar()
        tb.Entry(profile_frame, textvariable=self.password_var, show="*", width=40).grid(row=1, column=1, pady=5)

        tb.Label(profile_frame, text="Confirm Password:").grid(row=2, column=0, sticky="w", pady=5)
        self.confirm_password_var = tb.StringVar()
        tb.Entry(profile_frame, textvariable=self.confirm_password_var, show="*", width=40).grid(row=2, column=1, pady=5)

        tb.Button(profile_frame, text="Save Changes", bootstyle="success", command=self.save_profile).grid(
            row=3, column=0, columnspan=2, pady=15
        )

        # Logout Button
        tb.Button(self, text="Logout", bootstyle="danger", command=self.logout).pack(pady=(10, 5), anchor="e")

    def change_theme(self):
        new_theme = self.theme_var.get()
        try:
            self.style.theme_use(new_theme)
            messagebox.showinfo("Theme Changed", f"Theme switched to {new_theme}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to switch theme:\n{e}")

    def reset_theme(self):
        try:
            self.style.theme_use(self.default_theme)
            self.theme_var.set(self.default_theme)
            messagebox.showinfo("Theme Reset", f"Theme reset to default: {self.default_theme}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reset theme:\n{e}")

    def save_profile(self):
        email = self.email_var.get().strip()
        password = self.password_var.get()
        confirm_password = self.confirm_password_var.get()

        if not email:
            messagebox.showwarning("Validation Error", "Email cannot be empty.")
            return

        if password or confirm_password:
            if password != confirm_password:
                messagebox.showwarning("Validation Error", "Passwords do not match.")
                return
            if len(password) < 6:
                messagebox.showwarning("Validation Error", "Password should be at least 6 characters.")
                return

        try:
            conn = create_connection()
            cursor = conn.cursor()

            # Update email
            cursor.execute("UPDATE users SET email = %s WHERE username = %s", (email, self.username))
            self.user_data["email"] = email

            # Update password if provided
            if password:
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                cursor.execute("UPDATE users SET password = %s WHERE username = %s", (hashed_password, self.username))

            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "User profile updated successfully.")
            self.password_var.set("")
            self.confirm_password_var.set("")
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to update profile:\n{e}")

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.on_logout()
