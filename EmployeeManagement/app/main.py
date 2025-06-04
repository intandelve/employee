import ttkbootstrap as tb
from views.login_view import LoginView
from views.register_view import RegisterView
from views.dashboard_view import DashboardView
import ttkbootstrap as tb
from views.login_view import LoginView
from views.register_view import RegisterView


class App(tb.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.geometry("1700x900")
        self.current_view = None
        self.show_login()

    def clear_view(self):
        if self.current_view:
            self.current_view.destroy()

    def show_login(self):
        self.clear_view()
        self.current_view = LoginView(
            self,
            switch_to_register=self.show_register,
            switch_to_dashboard=self.show_dashboard  # ⬅️ Tambahkan ini
        )

    def show_register(self):
        self.clear_view()
        self.current_view = RegisterView(self, switch_to_login=self.show_login)

    def show_dashboard(self):
        self.clear_view()
        self.current_view = DashboardView(self)  # ⬅️ Ini untuk masuk dashboard

if __name__ == "__main__":
    app = App()
    app.mainloop()
