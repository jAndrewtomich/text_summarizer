from requests import get # http 'get' requests
from requests.exceptions import ConnectionError as RqConnError
import os # filesystem
import io # text encoding
from bs4 import BeautifulSoup # html parsing
from gensim.summarization.summarizer import summarize # extractive text summarization
from gensim.summarization import keywords # get keywords from summary


class NewsManager():
    def __init__(self, offset=0, url=None):
        self.url = url or os.environ["DEFAULT_HEADLINE_URL"]
        self.offset = offset
        self.hlList = self.extract_headlines()
        self.stride = len(self.hlList)

    def extract_headlines(self):
        hlList = []
        print("Extracting Stories ...")
        response = get(self.url)
        content = response.content
        soup = BeautifulSoup(content, "lxml")

        for tag in soup.find_all("td", attrs={"class": "title", "valign": ""}):
            if (link_url := tag.a["href"])[:4] != "http":
                link_url = "https://news.ycombinator.com/" + link_url
            
            hlList.append(link_url)
        
        return hlList[:-1]

    def generate_summaries(self):

        def get_only_text(url):
            try:
                page = get(url)
                soup = BeautifulSoup(page.content, "lxml")
                text = ' '.join(map(lambda p: p.text.strip(), soup.find_all('p')))
                title = "Default Title" if not soup.title else ' '.join(soup.title.stripped_strings)

            except RqConnError as e:
                title, text = None, e

            return title, text

        for i, hl in enumerate(self.hlList):
            title, text = get_only_text(hl)
            
            if title is None:
                print(f"Error : {hl} : {text}")
                continue

            k_l_words = keywords(text, ratio=0.1, lemmatize=True)

            try:
                summary = summarize(repr(text), ratio=0.1)
            except ValueError as e:
                summary = "Inadequate text structure.  This text cannot be summarized.  This is default text.  This might be summarized."

            out = f"{title}*<>*{summary}*<>*{k_l_words}*<>*{hl}"

            with io.open(f"output/output{i + (self.offset * self.stride)}.json", 'w', encoding='utf-8-sig') as writer:
                writer.write(out)
            
            if i == 29: return True
        
        return False