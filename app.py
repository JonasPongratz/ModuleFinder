import requests
from bs4 import BeautifulSoup

def follow_links(url, title, visited_links):

    # Alle Links mit passendem Titel in Liste packen
    links = extract_links(url, title)
    followed_links = []
    
    for link in links:
        if link in visited_links:
            continue
        visited_links.append(link)
        sub_links = follow_links(url, link, visited_links)
        followed_links.extend(sub_links)
    return links + followed_links

def extract_links(url, title):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    links = []
    for link in soup.find_all("a"):
        if title in link.get("title", ""):
            links.append(link.get("title"))

    return links

url = "https://portal.uni-kassel.de/qisserver/rds?state=wtree&search=1&trex=step&root120222=204790%7C204770%7C204976&P.vx=kurz"
all_links = follow_links(url, "Modul", [])

for x in all_links:
    print(x)