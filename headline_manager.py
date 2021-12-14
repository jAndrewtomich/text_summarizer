from requests import get
from bs4 import BeautifulSoup
import os


class HeadlineManager():
    def __init__(self, url=None):
        self.url = url or os.environ["DEFAULT_HEADLINE_URL"]

    def extract_headlines(self):
        hlList = []
        print("Extracting Stories ...")
        #cnt = ""
        #cnt += ("<b>Top Stories</b>\n" + "<br>" + '-' * 50 + "<br>")
        response = get(self.url)
        content = response.content
        soup = BeautifulSoup(content, "lxml")

        for i, tag in enumerate(soup.find_all("td", attrs={"class": "title", "valign": ""})):
            #cnt += ((str(i + 1) + " :: " + tag.text + "\n" + "<br>") if tag.text != "More" else "")
            hlList.append(tag.a["href"])
        
        return hlList[:-1]