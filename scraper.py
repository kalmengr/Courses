import requests
base_url = "https://freetutorials.se/"
base_search_url = "https://freetutorials.se/?s="
from bs4 import BeautifulSoup
import re
def search(query:str):
    results = []
    query:str = "+".join(query.split(" "))
    search_url = f"{base_search_url}{query}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, "html.parser")
    all_articles = soup.find_all("article", attrs={"class": "post-box"})
    for single_article in all_articles:
        course_url = single_article.find("a", attrs = {"rel":"bookmark"})
        response = requests.get(course_url["href"])
        soup = BeautifulSoup(response.text, "html.parser")
        torrent_link:str = soup.find("a", attrs= {"href": re.compile(r"(freetutorials\.se/wp-content/uploads|magnet)")})
        if torrent_link["href"].startswith("magnet"):
            magnet = True
        else:
            magnet = False
        results.append({"name": course_url["href"], "magnet": magnet, "link": torrent_link["href"]})
    return results
search("after effects")