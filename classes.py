import typer
import imaplib
import email
from email.header import decode_header
import unidecode

try_again_message = "Try again, be sure that the sender email exists."


class User:
    # Initializing the User class
    def __init__(self, username, password, mail_server):
        self.username = username
        self.password = password
        self.mail_server = mail_server

    # Connecting the user to the imapserver
    def initialize_user(self):
        # Making the imap var global, so the other functions use the same var
        global imap
        imap = imaplib.IMAP4_SSL(self.mail_server)
        imap.login(self.username, self.password)
        imap.select("INBOX")

    # The expunge function delete all mails flagged as DELETED by the delete_by_sender/subject functions.
    def delete_and_expunge(self):
        imap.expunge()
        imap.close()
        imap.logout()

    # Returning the option to delete new mails
    def reload_deletion(self):
        user_response = (
            input("Do you wan't to delete more items?(y/n)\n").lower().strip()
        )
        if user_response == "n":
            self.delete_and_expunge()
            typer.echo("Thanks, until next time!")
            typer.Exit(0)

        if user_response == "y":
            self.deletion_parent()

    # The main deletion function, utilizes the other ones to work
    def deletion_parent(self):
        user_response = (
            typer.prompt(
                "Do you wish to search by subject or by sender? (type: subject(s), sender(sd) or quit(q))"
            )
            .lower()
            .strip()
        )

        # Refactor this into a function
        if user_response == "sd":
            try:
                self.delete_by_sender()

            except TypeError:
                print(try_again_message)

        elif user_response == "s":
            try:
                self.delete_by_subject()
            except TypeError:
                print(try_again_message)
        elif user_response == "q":
            typer.secho("Until the next time!", fg=typer.colors.GREEN)
            raise typer.Exit(0)

        else:
            print("Be sure to type a valid answer")
            self.deletion_parent()

    # Flagg the selected mails as DELETED
    def delete_by_sender(self):
        sender = input("Enter the sender mail address: ").lower().strip()
        try:
            status, messages = imap.search(None, f"FROM {sender}")
            messages = messages[0].split(b" ")
            # Loop to iterate over targeted mails and mark them as deleted
            for mail in messages:
                _, msg = imap.fetch(mail, "(RFC822)")
                self.show_messages_topics(msg)

                # Marking the mail as deleted
                imap.store(mail, "+FLAGS", "\\Deleted")
            print("Deletion successeful!")
        except:
            typer.secho(f"Error, try again.", err=True, fg=typer.colors.GREEN)
            self.delete_by_sender()
        self.reload_deletion()

    # Flagg the selected mails as DELETED - Maybe refactor this two functions into a third one with the concept(Interfaces in golang)
    def delete_by_subject(self):
        subject = input("Enter the subject key-words: ")
        subject_unaccented = unidecode.unidecode(subject)
        status, messages = imap.search(None, f"SUBJECT {subject_unaccented}")
        try:
            messages = messages[0].split(b" ")
            # Loop to iterate over targeted mails and mark them as deleted
            for mail in messages:
                _, msg = imap.fetch(mail, "(RFC822)")
                # This second loop is only for printing the SUBJECT of targeted mails
                self.show_messages_topics(msg)

                # Marking the mail as deleted
                imap.store(mail, "+FLAGS", "\\Deleted")
            print("Deletion successeful!")
        except:
            typer.secho(f"Error, try again.", err=True, fg=typer.colors.GREEN)
            self.delete_by_subject()
        self.reload_deletion()

    def delete_by_date(self):
        since_date_input = ("Enter the desired initial date(ex:01-jan-2020): ").upper().strip()
        before_date_input = ("Enter the desired end date(ex:01-jan-2020): ").upper().strip()
        status, messages = imap.search(None, f'SINCE "{since_date_input}" BEFORE "{before_date_input}"')
        try:
            messages = messages[0].split(b" ")
            # Loop to iterate over targeted mails and mark them as deleted
            for mail in messages:
                _, msg = imap.fetch(mail, "(RFC822)")
                # This second loop is only for printing the SUBJECT of targeted mails
                self.show_messages_topics(msg)

                imap.store(mail, "+FLAGS", "\\Deleted")
            print("Deletion successeful!")
        except:
            typer.secho(f"Error, try again.", err=True, fg=typer.colors.GREEN)
            self.delete_by_subject()
        self.reload_deletion()

    # Decode the bytes header messages into a redable format
    def show_messages_topics(self, messages):
        for response in messages:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                # Decoding the mail subject
                subject = decode_header(msg["Subject"])[0][0]
                if isinstance(subject, bytes):
                    # If it is a bytes type, decode to str
                    subject = subject.decode()
                print("Deleting", subject)
