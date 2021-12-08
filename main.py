import funcs # import our functions
import os # filesystem and environment variables
import datetime # system time for record keeping
from dotenv import load_dotenv # load environment variables
load_dotenv() #   -   -   -   -   -   -   -   -   -   -   |

def main():
    now = datetime.datetime.now()
    content = ""

    cnt = funcs.extract_news(input("Enter URL: ") or os.environ["DEFAULT_NEWS_URL"])
    content += cnt
    content += ("<br>------<br>")
    content += ("<br><br>End of Message")

    """
    get text from target url
    """
    text = funcs.get_only_text( \
        input("Enter URL: ") or \
        os.environ["DEFAULT_TARGET_URL"]) # use default url from env variables if no input

    """
    display link text and text length
    """ 
    print(len(text)) # length of tuple
    print(len(str.split(text[1]))) # number of words in link text, aside from title
    print(text) # full text of link

    """
    summarize text
    """
    txt_summ = funcs.summ(text) # call summarizer
    print(txt_summ) # view output

    """
    produce keywords from summary
    """
    k_words = funcs.get_keyword_lemmas(text) # get lemmatized keywords
    print(k_words) # view output


if __name__ == "__main__":
    main()
