import requests
from bs4 import BeautifulSoup
import re

# Start url (could be "Module Masterstudiengang Informatik (PO2012)")
url = "https://portal.uni-kassel.de/qisserver/rds?state=wtree&search=1&trex=step&root120222=204790%7C204770%7C204976&P.vx=kurz"
searched_tag = "^Modul."

def follow_links(url, searched_tag, depth):
    followed_links = []
    visited_links = []
    # Search the html doc for all links with a title containing "Modul"
    links = extract_links(url, searched_tag)

    for link in links:
        if link in visited_links:
            continue
        visited_links.append(link)
        if depth != 0:
            depth -= 1
            sub_links = follow_links(link[0], searched_tag, depth)
            followed_links.extend(sub_links)
    return links + followed_links

def extract_links(url, searched_tag):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    links = []
    for link in soup.find_all("a"):
        if re.search(searched_tag, link.get("title", "")):
            links.append([link.get("href"),link.get("title")])
    return links


all_links = follow_links(url,searched_tag, 4)

for x in all_links:
    print(x[1])