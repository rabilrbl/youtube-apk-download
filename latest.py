from cgitb import text
from bs4 import BeautifulSoup as bs
import requests
import os

# from dotenv import load_dotenv

# load_dotenv()


class Latest:
    def __init__(self, name: str):
        self.name = name
        self.host_url = "https://www.apkmirror.com"
        self.url = f"/apk/google-inc/{self.name}/"
        self.headers = {
            "authority": "www.apkmirror.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "en-IN,en-GB;q=0.9,en;q=0.8,en-US;q=0.7",
            "cache-control": "max-age=0",
            "dnt": "1",
            "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47",
        }

    def __str__(self):
        return self.name

    def req(self, url: str | None = None, soup: bool = True):
        """
        Request the page and returns beautiful soup object
        """
        url = url if url else self.url
        print(f"Making request to {url}")
        req = requests.get(f"{self.host_url}{url}", headers=self.headers)
        if soup:
            return bs(req.content, "html.parser")
        return req
    
    def create_url(self, url: str):
        return f"{self.host_url}{url}"

    def latest_version(self) -> str:
        print("\nGetting latest version of", self.name)
        page = self.req()
        parents = page.find("a", {"class": "downloadLink"})
        url = parents["href"]
        page = self.req(url)

        for comp in page.find_all("div", {"class": "table-row headerFont"}):
            if "nodpi" in comp.text:
                url = comp.find("a", {"class": "accent_color"})["href"]

        page = self.req(url)
        url = page.find("a", {"rel": "nofollow", "class":"accent_bg"})["href"]

        page = self.req(url)
        url = page.find("a", {"rel": "nofollow"}, text="here")["href"]

        print(f"Download Link for {self.name} is {self.create_url(url)}")

        return self.create_url(url)
        
    def download(self, url: str, path: str = "./"):
        print("\nDownloading", self.name)
        req = requests.get(url, headers=self.headers)
        with open(f"{path}{self.name}.apk", "wb") as f:
            f.write(req.content)
        print(f"Downloaded {self.name} to {path}")
        return True


