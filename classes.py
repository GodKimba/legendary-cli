import typer
import imaplib
import email
from email.header import decode_header


try_again_message = "Try again, be sure that the sender email exists."


class User:
    def __init__(self, username, password, mail_server):
        self.username = username
        self.password = password
        self.mail_server = mail_server

    def initialize_user(self):
        global imap
        imap = imaplib.IMAP4_SSL(self.mail_server)
        imap.login(self.username, self.password)
        imap.select("INBOX")

    def delete_and_expunge(self):
        imap.expunge()
        imap.close()
        imap.logout()
        typer.secho("Thanks, until the next time!", color="GREEN")
        typer.Exit(code=0)

    def reload_deletion(self):
        user_response = (
            input("Do you wan't to delete more items?(y/n)\n").lower().strip()
        )
        if user_response == "n":
            self.delete_and_expunge()

        if user_response == "y":
            self.deletion_parent()

    def deletion_parent(self):
        user_response = (
            typer.prompt(
                "Do you wish to search by subject or by sender? (type: subject, sender or quit)"
            )
            .lower()
            .strip()
        )

        if user_response == "sender":
            try:
                self.delete_by_sender()

            except TypeError:
                print(try_again_message)

        elif user_response == "subject":
            try:
                self.delete_by_subject()
            except TypeError:
                print(try_again_message)
        elif user_response == "quit":
            typer.secho("Until the next time!", fg=typer.colors.GREEN)
            raise typer.Exit(0)

        else:
            print("Be sure to type a valid answer")
            self.deletion_parent()

    def delete_by_sender(self):
        sender = input("Enter the sender mail address: ").lower().strip()
        try:
            status, messages = imap.search(None, f"FROM {sender}")
            messages = messages[0].split(b" ")
            # Loop to iterate over targeted mails and mark them as deleted
            for mail in messages:
                _, msg = imap.fetch(mail, "(RFC822)")
                # This second loop is only for printing the SUBJECT of targeted mails
                for response in msg:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])
                        # Decoding the mail subject
                        subject = decode_header(msg["Subject"])[0][0]
                        if isinstance(subject, bytes):
                            # If it is a bytes type, decode to str
                            subject = subject.decode()
                        print("Deleting", subject)
                # Marking the mail as deleted
                imap.store(mail, "+FLAGS", "\\Deleted")
            print("Deletion successeful!")
        except:
            typer.secho(f"Error, try again.", err=True, fg=typer.colors.GREEN)
            raise typer.Exit(0)
            self.delete_by_sender()
        self.reload_deletion()

    def delete_by_subject(self):
        subject = input("Enter the subject key-words: ")
        status, messages = imap.search(None, f"SUBJECT {subject}")
        try:
            messages = messages[0].split(b" ")
            # Loop to iterate over targeted mails and mark them as deleted
            for mail in messages:
                _, msg = imap.fetch(mail, "(RFC822)")
                # This second loop is only for printing the SUBJECT of targeted mails
                for response in msg:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])
                        # Decoding the mail subject
                        subject = decode_header(msg["Subject"])[0][0]
                        if isinstance(subject, bytes):
                            # If it is a bytes type, decode to str
                            subject = subject.decode()
                        print("Deleting", subject)
                # Marking the mail as deleted
                imap.store(mail, "+FLAGS", "\\Deleted")
            print("Deletion successeful!")
        except:
            typer.secho(f"Error, try again.", err=True, fg=typer.colors.GREEN)
            self.delete_by_subject()
        self.reload_deletion()

    def delete_by_date(self):

        status, messages = imap.search(None, 'SINCE "01-JAN-2020"')
        try:
            messages = messages[0].split(b" ")
            # Loop to iterate over targeted mails and mark them as deleted
            for mail in messages:
                _, msg = imap.fetch(mail, "(RFC822)")
                # This second loop is only for printing the SUBJECT of targeted mails
                for response in msg:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])
                        # Decoding the mail subject
                        subject = decode_header(msg["Subject"])[0][0]
                        if isinstance(subject, bytes):
                            # If it is a bytes type, decode to str
                            subject = subject.decode()
                        print("Deleting", subject)
                # Marking the mail as deleted
                imap.store(mail, "+FLAGS", "\\Deleted")
            print("Deletion successeful!")
        except:
            typer.secho(f"Error, try again.", err=True, fg=typer.colors.GREEN)
            self.delete_by_subject()
        self.reload_deletion()
