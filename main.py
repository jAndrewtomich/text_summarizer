from dotenv import load_dotenv # load environment variables

from os.path import dirname, join # get path to .env file

import sys # argv
import os # check validity of filenames, delete output file
import validators # check urls

#from headline_manager import HeadlineManager # Each valid url (either from input file or command line args) will be scraped for headline links
#from email_manager import EmailManager # Create and send emails
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

    if os.path.isdir("output"): 
        for f in os.listdir("output"):
            os.remove(f"output/{f}")
        os.rmdir("output") # remove any old copy of output to avoid duplicate information

    os.mkdir("output")

    for i, site in enumerate(news_sites):
        news_m = NewsManager(i) if not site else NewsManager(i, site.strip())

        print(news_m.generate_summaries())


if __name__ == "__main__":
    main()