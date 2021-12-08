from requests import get # http 'get' requests
from bs4 import BeautifulSoup # html parsing
from gensim.summarization.summarizer import summarize # extractive text summarization
from gensim.summarization import keywords # get keywords from summary


def extract_news(url):
    print("Extracting Stories...")
    cnt = ""
    cnt += ("<b>Top Stories</b>\n" + "<br>" + '-' * 50 + "<br>")
    response = get(url)
    content = response.content
    soup = BeautifulSoup(content, "lxml")

    for i, tag in enumerate(soup.find_all("td", attrs={"class": "title", "valign": ""})):
        cnt += ((str(i + 1) + " :: " + tag.text + "\n" + "<br>") if tag.text != "More" else "")

    return cnt


def get_only_text(url):
    """
    return title and text of article at target url.
    """
    page = get(url)
    soup = BeautifulSoup(page.content, "lxml")
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    #text = list(map(lambda p: p.text, soup.find_all('p')))[0]
    title = ' '.join(soup.title.stripped_strings)

    return title, text


def summ(text):
    """
    return title and summarization of target url
    """
    heading = f"Title : {text[0]}\nSummary : "
    summary = summarize(repr(text), ratio=0.1)

    return heading + "\n" + summary
    

def get_keyword_lemmas(text):
    """
    return lemmatized keywords from summary
    """
    k_l_words = keywords(text[1], ratio=0.1, lemmatize=True)

    return f"\nKeywords:\n{k_l_words}"


