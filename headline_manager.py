from requests import get
from bs4 import BeautifulSoup
import os


class HeadlineManager():
    def __init__(self, url=None):
        self.url = url or os.environ["DEFAULT_HEADLINE_URL"]

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