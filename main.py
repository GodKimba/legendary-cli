import os
import typer
from decouple import config
from classes import User

app = typer.Typer()

# # Environment variables to hide the default value from cli
# os.environ["USERNAME"] = config("USERNAME")
# os.environ["PASSWORD"] = config("PASSWORD")

# Still need to change the way that the default user is set
# Fix the error from searching non existing keys words
# I think is better to use @app.command() to have a cleaner and more efficient code
# Need to create another file to store the classes


def check_if_empty(item_to_check):
    pass


def create_user_file():
    username = input("Enter your gmail address: ").lower().strip()
    typer.secho(
        "If you don't have a application passowrd yet, follow these instructions: https://support.google.com/accounts/answer/185833?hl=en",
        fg=typer.colors.GREEN,
    )
    password = typer.prompt("Enter your application password: ")

    with open(".env", "w") as file:
        file.write(f"USERNAME={username}\n")
        file.write(f"PASSWORD={password}")


def main():
    if not os.path.exists(".env"):
        create_user_file()

    primary_user = User(
        username=config("USERNAME"),
        password=config("PASSWORD"),
        mail_server="imap.gmail.com",
    )

    primary_user.initialize_user()
    primary_user.deletion_parent()


if __name__ == "__main__":
    typer.run(main)
