import requests
from bs4 import BeautifulSoup
import json
import os

URL = "http://zs1mm.home.pl/plan/lista.html"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

sale = soup.find_all("a", href=lambda text: "plany/s" in text.lower())
nauczyciel = soup.find_all("a", href=lambda text: "plany/n" in text.lower())

nauczyciele = {}


def skrot():
    for e in nauczyciel:
        url2 = "http://zs1mm.home.pl/plan/" + e["href"]
        plan = requests.get(url2)
        soup12 = BeautifulSoup(plan.content, "html.parser")
        ok = soup12.find("span", class_="tytulnapis")
        ok2 = str(ok.contents[0]).replace(" -", "-")
        ok3 = ok2.replace("- ", "-")
        nauczyciele[ok3[-3:-1]] = ok3[:-4].strip()


saledata = {}


def saleget():
    for element in sale:
        url2 = "http://zs1mm.home.pl/plan/" + element["href"]
        plan = requests.get(url2)
        soup2 = BeautifulSoup(plan.content, "html.parser")
        tabela = soup2.find("table", class_="tabela")
        days = [{}, {}, {}, {}, {}]
        for ele in tabela.find_all("tr"):
            nr = ele.find("td", class_="nr")
            if nr is not None:
                tds = ele.find_all("td", class_="l")
                for i in range(len(tds)):
                    if tds[i].contents[0] == '\xa0':
                        days[i][nr.contents[0]] = None
                    else:
                        try:
                            lekcja = None
                            for j in range(4, 11, 2):
                                try:
                                    if tds[i].contents[j].name == "span":
                                        lekcja = tds[i].contents[j].contents[0]
                                        break
                                except:
                                    pass
                            klasy = []
                            for index in range(2, 9, 2):
                                try:
                                    if tds[i].contents[index].name == "a":
                                        klasy.append(tds[i].contents[index].contents[0])
                                except:
                                    pass
                            days[i][nr.contents[0]] = [[nauczyciele[tds[i].contents[0].contents[0]], tds[i].contents[0].contents[0]], klasy, lekcja]
                        except:
                            days[i][nr.contents[0]] = "Broken data"
        saledata[element.contents[0]] = days


def update():
    skrot()
    saleget()

    jsonstr = json.dumps(saledata)
    with open(os.path.realpath(os.path.dirname(__file__)) + "\\data.json", "w") as f:
        f.write(jsonstr)
        f.close()

    jsonstr2 = json.dumps(nauczyciele)
    with open(os.path.realpath(os.path.dirname(__file__)) + "\\teach.json", "w") as f:
        f.write(jsonstr2)
        f.close()


if __name__ == '__main__':
    update()
