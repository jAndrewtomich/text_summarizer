from dotenv import load_dotenv # load environment variables

from os.path import dirname, join # get path to .env file

from headline_manager import HeadlineManager
from email_manager import EmailManager
from news_manager import NewsManager

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

import sys
import os


def main():

    if len((args := sys.argv)) > 1:
        if os.path.isfile(args[1]):
            with open(args[1], 'r') as reader:
                news_sites = reader.readlines()
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
                writer.write(txt_summ + "\n")

            """
            produce keywords from summary
            """
            k_words = news_m.get_keyword_lemmas() # get lemmatized keywords
            with open("output.txt", 'a') as writer:
                writer.write(k_words + "**")

    with open("output.txt", 'r') as reader:
        full_text = reader.read()

    email_m = EmailManager()
    email_m.send_email(full_text)


if __name__ == "__main__":
    main()



