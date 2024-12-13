from datetime import datetime

class User:
    def __init__(self, username: str, email: str, password: str, active: bool, theme: str = None):
        self.username = username
        self.email = email
        self.password = password
        self.active = active
        self.theme = theme
        self.created_at = datetime.now()

    def display(self):
        """Display user information in the console."""
        return {
            "Username": self.username,
            "Email": self.email,
            "Active": self.active,
            "Theme": self.theme or "Default",
            "Created At": self.created_at.strftime("%d/%m/%Y"),
        }

def create_example_user():
    example_user = User(
        username="Naveen123",
        email="naveen@example.com",
        password="securepassword123",
        active=True,
    )
    print(example_user.display())

create_example_user()
