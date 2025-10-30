import requests, xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from datetime import datetime
from hashlib import md5

URL = "https://www.audible.com/search?searchNarrator=Jefferson+Mays&sort=pubdate-desc-rank"
headers = {"User-Agent":"Mozilla/5.0 (compatible; feedbot/1.0)"}

r = requests.get(URL, headers=headers)
soup = BeautifulSoup(r.text, "lxml")

rss = ET.Element("rss", version="2.0")
ch = ET.SubElement(rss, "channel")
ET.SubElement(ch, "title").text = "Jefferson Mays – Audible new releases"
ET.SubElement(ch, "link").text = URL
ET.SubElement(ch, "description").text = "Automatically generated feed from Audible search results."

for item in soup.select("li.adbl-impression-container"):
    title = item.select_one("h3")
    link = item.select_one("a[href*='/pd/']")
    if not (title and link): 
        continue
    title_text = title.get_text(strip=True)
    href = "https://www.audible.com" + link["href"]
    guid = md5(href.encode()).hexdigest()
    e = ET.SubElement(ch, "item")
    ET.SubElement(e, "title").text = title_text
    ET.SubElement(e, "link").text = href
    ET.SubElement(e, "guid").text = guid
    ET.SubElement(e, "pubDate").text = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

open("feed.xml", "wb").write(ET.tostring(rss, encoding="utf-8"))
print("✅ Feed built successfully.")
