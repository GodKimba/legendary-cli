import typer
import imaplib
import email
from email.header import decode_header
from decouple import config
from enum import Enum
from classes import User
import os

# # Environment variables to hide the default value from cli
# os.environ["USERNAME"] = config("USERNAME")
# os.environ["PASSWORD"] = config("PASSWORD")

# # Using envvar for lack of better tool
# def main(
#     user: str = typer.Option(
#         None,
#         envvar=["USERNAME"],
#         show_envvar=False,
#         prompt="Please, insert your mail account",
#     ),
#     password: str = typer.Option(
#         None,
#         envvar=["PASSWORD"],
#         prompt="Please insert your mail password",
#         hide_input=True,
#         show_envvar=False,
#     ),
# ):

#     mail_server = "imap.gmail.com"
#     imap = imaplib.IMAP4_SSL(mail_server)
#     imap.login(user, password)
#     imap.select("inbox")

    
#     def delete_and_expunge():
#         imap.expunge()
#         imap.close()
#         imap.logout()

#     def delete_by_sender():
#         sender = input("Enter the sender mail address: ").lower().strip()
#         status, messages = imap.search(None, f"FROM {sender}")
#         messages = messages[0].split(b" ")
#         # Loop to iterate over targeted mails and mark them as deleted
#         for mail in messages:
#             _, msg = imap.fetch(mail, "(RFC822)")
#             # This second loop is only for printing the SUBJECT of targeted mails
#             for response in msg:
#                 if isinstance(response, tuple):
#                     msg = email.message_from_bytes(response[1])
#                     # Decoding the mail subject
#                     subject = decode_header(msg["Subject"])[0][0]
#                     if isinstance(subject, bytes):
#                         # If it is a bytes type, decode to str
#                         subject = subject.decode()
#                     print("Deleting", subject)
#             # Marking the mail as deleted
#             imap.store(mail, "+FLAGS", "\\Deleted")
#         print("Deletion successeful!")
#         reload_deletion()


#     def delete_by_subject():
#         subject = input("Enter the subject key-words: ").lower().strip()
#         status, messages = imap.search(None, f"SUBJECT {subject}")
#         messages = messages[0].split(b" ")
#         # Loop to iterate over targeted mails and mark them as deleted
#         for mail in messages:
#             _, msg = imap.fetch(mail, "(RFC822)")
#             # This second loop is only for printing the SUBJECT of targeted mails
#             for response in msg:
#                 if isinstance(response, tuple):
#                     msg = email.message_from_bytes(response[1])
#                     # Decoding the mail subject
#                     subject = decode_header(msg["Subject"])[0][0]
#                     if isinstance(subject, bytes):
#                         # If it is a bytes type, decode to str
#                         subject = subject.decode()
#                     print("Deleting", subject)
#             # Marking the mail as deleted
#             imap.store(mail, "+FLAGS", "\\Deleted")
#         print("Deletion successeful!")
#         reload_deletion()

#     # Need to put all of this inside a function
#     def deletion_parent():
#         user_response = (
#             typer.prompt(
#                 "Do you wish to search by subject or by sender? (type: subject, sender or quit)"
#             )
#             .lower()
#             .strip()
#         )

#         if user_response == "sender":
#             try:
#                 delete_by_sender()

#             except TypeError:
#                 print("Try again, be sure that the sender email exists.")

#         elif user_response == "subject":
#             try:
#                 delete_by_subject()
#             except TypeError:
#                 print("Try again, be sure that the subject key words exists.")
#         else:
#             print("Be sure to type a valid answer")
#             main()

    
#     def reload_deletion():
#         user_response = input("Do you wan't to delete more items?(y/n)").lower().strip()
#         if user_response == "n":
#             delete_and_expunge()

#         if user_response == "y":
#             deletion_parent()
    
#     deletion_parent()    
#     delete_and_expunge()


# if __name__ == "__main__":
#     typer.run(main)


# # Still need to change the way that the default user is set
# # Fix the error from searching non existing keys words


def create_user_file():
    username = input("Enter your mail address: ").lower().strip()
    password = input("Enter your password: ")

    with open(".env", "w") as file:
        file.write(f"USERNAME={username}\n")
        file.write(f"PASSWORD={password}")

def main():
    if not os.path.exists(".env"):
        create_user_file()
    
    primary_user = User(username = config("USERNAME"), password=config("PASSWORD"), mail_server="imap.gmail.com")

    primary_user.initialize_user()
    primary_user.deletion_parent()
    primary_user.reload_deletion()

        


if __name__ == "__main__":
    typer.run(main)
