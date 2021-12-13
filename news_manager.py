from requests import get # http 'get' requests
import os
from bs4 import BeautifulSoup # html parsing
from gensim.summarization.summarizer import summarize # extractive text summarization
from gensim.summarization import keywords # get keywords from summary


class NewsManager():
    def __init__(self, url=None):
        url = url or os.environ["DEFAULT_NEWS_URL"]

        def get_only_text(url):
            page = get(url)
            soup = BeautifulSoup(page.content, "lxml")
            text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
            title = ' '.join(soup.title.stripped_strings)

            return title, text

        title, text = get_only_text(url)

        self.title = title
        self.text = text

    def summ(self):
        heading = f"Title : {self.title}\nSummary : "
        summary = summarize(repr(self.text), ratio=0.2)

        return heading + "\n" + summary

    def get_keyword_lemmas(self):
        k_l_words = keywords(self.text, ratio=0.7, lemmatize=True)

        return f"\nKeywords:\n{k_l_words}"