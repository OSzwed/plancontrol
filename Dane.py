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
        URL = "http://zs1mm.home.pl/plan/"+e["href"]
        plan = requests.get(URL)
        soup12 = BeautifulSoup(plan.content, "html.parser")
        ok = soup12.find("span",class_="tytulnapis")
        ok2 = str(ok.contents[0]).replace(" -", "-")
        ok3 = ok2.replace("- ","-")
        nauczyciele[ok3[-3:-1]] = ok3[:-4].strip()


saledata = {}

def saleget():
    for element in sale:
        URL = "http://zs1mm.home.pl/plan/"+element["href"]
        plan = requests.get(URL)
        soup2 = BeautifulSoup(plan.content, "html.parser")
        tabela = soup2.find("table", class_="tabela")
        days = [{},{},{},{},{}]
        for ele in tabela.find_all("tr"):
            nr = ele.find("td", class_="nr")
            if nr != None:
                tds = ele.find_all("td", class_="l")
                for i in range(len(tds)):
                    if tds[i].contents[0] == '\xa0':
                        days[i][nr.contents[0]] = None
                    else:
                        try:
                            days[i][nr.contents[0]] = [[nauczyciele[tds[i].contents[0].contents[0]],tds[i].contents[0].contents[0]],tds[i].contents[2].contents[0]]
                            #,tds[i].contents[4].contents[0]
                        except:
                            days[i][nr.contents[0]] = "Broken data"
        saledata[element.contents[0]] = days

def update():
    skrot()
    saleget()

    jsonstr = json.dumps(saledata)
    with open(os.path.realpath(os.path.dirname(__file__))+"\data.json", "w") as f:
        f.write(jsonstr)
        f.close()

update()
