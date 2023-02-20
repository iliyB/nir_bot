import requests
from bs4 import BeautifulSoup


class google_search:
    def __init__(self, web_society, **kwargs):
        self.params_all = kwargs.keys()
        self.params = ""
        for i in self.params_all:
            if i != None:
                if isinstance(kwargs.get(i), list):
                    self.params = self.params + " ".join(set(kwargs.get(i)))

                self.params = self.params + " " + str(kwargs.get(i))

        self.params = self.params.replace(" ", "+")

        self.headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
        }
        self.google_link = "https://google.com/search?q="
        self.web_society = web_society

    def search_web_society(self):
        request = self.google_link + "inurl:" + self.web_society + "+" + self.params
        response = requests.get(request, headers=self.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            results = []
            for g in soup.find_all("div", class_="yuRUbf"):
                anchors = g.find_all("a")
                if anchors:
                    link = anchors[0]["href"]
                    title = ""
                    if g.find("h3") != None:
                        # print("H3", g.find('h3'))
                        title = g.find("h3").text
                        # print(title)
                    item = {"title": title, "link": link}
                    results.append(item)
            return results

    def search_all(self):
        request = self.google_link + self.params
        print("Запрос", request)
        response = requests.get(request, headers=self.headers)
        print("статус", response)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            results = []
            for g in soup.find_all("div", class_="yuRUbf"):
                anchors = g.find_all("a")
                if anchors:
                    link = anchors[0]["href"]
                    title = ""
                    if g.find("h3") is True:
                        title = g.find("h3").text
                        print(title)
                    item = {"title": title, "link": link}
                    results.append(item)
            print("Ответ", results)


if __name__ == "__main__":
    temp = google_search(name="Юрий Монахов", city="Владимир").search_web_society()
