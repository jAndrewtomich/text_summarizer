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
            text = ' '.join(map(lambda p: p.text.strip(), soup.find_all('p')))
            title = "Default Title" if not soup.title else ' '.join(soup.title.stripped_strings)

            return title, text

        title, text = get_only_text(url)

        self.title = title
        self.text = text

    def summ(self):
        heading = "Title : <b>" + self.title + "</b><br>Summary : <br>"

        try:
            summary = summarize(repr(self.text), ratio=0.2)
            return heading + summary
        except ValueError as e:
            return "Text cannot be summarized: inappropriate structure.  Text must have more than one sentence."

    def get_keyword_lemmas(self):
        k_l_words = keywords(self.text, ratio=0.2, lemmatize=True)

        return f"Keywords:\n{k_l_words}\n"