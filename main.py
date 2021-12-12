from dotenv import load_dotenv # load environment variables

from os.path import dirname, join # get path to .env file

from headline_manager import HeadlineManager
from email_manager import EmailManager
from news_manager import NewsManager

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


def main():
    headline_m = HeadlineManager()
    headlines = headline_m.extract_headlines()

    email_m = EmailManager()
    #email_m.send_email(headlines)
    
    news_m = NewsManager(url="https://www.voxmedia.com/2021/11/19/22791332/the-second-season-of-vox-and-vox-media-studios-the-mind-explained-premieres-today-on-netflix")

    """
    display link text and text length
    """ 
    print(len(news_m.text)) # length of string
    print(len(str.split(news_m.text))) # number of words in link text, aside from title
    print(news_m.text) # full text of link

    """
    summarize text
    """
    txt_summ = news_m.summ() # call summarizer
    print(txt_summ) # view output

    """
    produce keywords from summary
    """
    k_words = news_m.get_keyword_lemmas() # get lemmatized keywords
    print(k_words) # view output


if __name__ == "__main__":
    main()



