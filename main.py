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

    if len((args := sys.argv)) > 1:
        if os.path.isfile(args[1]):
            with open(args[1], 'r') as reader:
                news_sites = reader.readlines()
        elif validators.url(args[1]):
            news_sites = [args[1]]
        else:
            print("Error: Invalid arguments")
    else:
        news_sites = [None]

    for site in news_sites:
        headline_m = HeadlineManager(site.strip())
        headlines, hlList = headline_m.extract_headlines()

        for hl in hlList: 
            news_m = NewsManager(hl) if hl else NewsManager()

            """
            summarize text
            """
            txt_summ = news_m.summ() # call summarizer
            with open("output.txt", 'a') as writer:
                writer.write(txt_summ)

            """
            produce keywords from summary
            """
            k_words = news_m.get_keyword_lemmas() # get lemmatized keywords
            with open("output.txt", 'a') as writer:
                writer.write(k_words)

    with open("output.txt", 'r') as reader:
        full_text = reader.read()

    print(headlines)
    print(full_text)
    #email_m = EmailManager()
    #email_m.send_email(full_text)
    os.remove("output.txt")


if __name__ == "__main__":
    main()



