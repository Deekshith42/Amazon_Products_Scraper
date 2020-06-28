from selectorlib import Extractor
import requests
import json
from time import sleep

e = Extractor.from_yaml_file("selectors.yml")

def scrape(url):
    headers ={
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers = headers)
    # Simle check to check if page was blocked
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by amazon.Try using better proxies\n"%url)
        else:
            print("Page %s was blocked by amazon as the status code was %d"%(url,r.status_code))
        return None

    # Pass the html page and create text file
    return e.extract(r.text)

with open("urls.txt","r") as urlist,open("output.jsnol","w") as outfile:
    for url in urlist.readlines():
        data = scrape(url)
        if data:
            json.dump(data,outfile)
            outfile.write("\n")
            sleep(5)
