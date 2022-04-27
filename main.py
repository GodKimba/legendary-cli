import typer
import imaplib
import email
from email.header import decode_header
from decouple import config


def main(user: str = typer.Argument(..., prompt="Please, insert your mail account"), password: str = typer.Option(..., prompt="Please insert your mail password")):
    
    mail_server = "imap.gmail.com"
    imap = imaplib.IMAP4_SSL(mail_server)
    imap.login(user, password)
    imap.select("inbox")

    def delete_by_sender():
        sender = input("Enter the sender mail address: ").lower().strip()
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

    def delete_by_subject():
        subject = input("Enter the subject key-words: ").lower().strip()
        status, messages = imap.search(None, f"SUBJECT {subject}")
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


    user_response = typer.prompt("Do you wish to search by subject or by sender? (type: subject, sender or quit:\n").lower().strip()

    if user_response == "sender":
        try:
            delete_by_sender()

        except TypeError:
            print("Try again, be sure that the sender email exists.")


    elif user_response == "subject":
        try:
            delete_by_subject()
        except TypeError:
            print("Try again, be sure that the subject key words exists.")
    else:
        print("Be sure to type a valid answer")
        main()


    imap.expunge()
    imap.close()
    imap.logout()

if __name__ == "__main__":
    typer.run(main)