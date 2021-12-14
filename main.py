from dotenv import load_dotenv # load environment variables

from os.path import dirname, join # get path to .env file

import sys # argv
import os # check validity of filenames, delete output file
import validators # check urls

from headline_manager import HeadlineManager # Each valid url (either from input file or command line args) will be scraped for headline links
from email_manager import EmailManager # Create and send emails
from news_manager import NewsManager # Perform text summarization and extract keywords from each article

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


def main():

    if len((args := sys.argv[1:])) >= 1: # check for command line arguments
        if os.path.isfile(args[0]): # if arguments are present, check if first arg is filename.  If so, read contents of file as args.
            with open(args[0], 'r') as reader:
                news_sites = reader.readlines()
        else:
            news_sites = [a for a in args if validators.url(a)] # urls can be presented as a space separated list at command line
    else:
        news_sites = [None] # default value

    if os.path.isfile("output.txt"): os.remove("output.txt") # remove any old copy of output to avoid duplicate information

    for site in news_sites:

        headline_m = HeadlineManager() if not site else HeadlineManager(site.strip())

        for hl in headline_m.hlList:
            news_m = NewsManager(hl)

            """
            summarize text
            """
            txt_summ = news_m.summ() # call summarizer
            with open("output.txt", 'a') as writer: # write to temporary output file so results can be more easily concatenated
                writer.write(txt_summ + "\n" + "<br>")

            """
            produce keywords from summary
            """
            k_words = news_m.get_keyword_lemmas() # get lemmatized keywords
            with open("output.txt", 'a') as writer:
                writer.write(k_words + "\n" + "<br>------<br>")

            del news_m # cleanup memory
        del headline_m # cleanup memory

    with open("output.txt", 'r') as reader: # concatenate output in order to send in single email
        full_text = reader.read()

    email_m = EmailManager() # create email from total output
    email_m.send_email(full_text)

    os.remove("output.txt") # delete output file


if __name__ == "__main__":
    main()



