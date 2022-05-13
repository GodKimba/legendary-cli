# legendary-cli
Python Script that uses the imap library to clean up bulk emails using keywords or mail addresses.

## Installation
It's as easy as cloning the repo and running the script

## User Configuration
The script uses a .env file to store locally your mail credentials, if you're using gmail the script will automatically guide your through the config.
(If you want to use other mail services you need to change the hardcoded info)

## Observations - Known Bugs:
- The gmail server don't accept spaced keywords, so if you try to use more than one the script will ask you to try again.
- Accented letters won't work. I already tried to convert the accented letters and the script will continue to run but probably won't find what you're looking for.

