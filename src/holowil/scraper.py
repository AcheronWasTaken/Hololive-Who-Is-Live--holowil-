from bs4 import BeautifulSoup
import json
import requests as req
import re
from tqdm import tqdm as progress
from pathlib import Path

cwd = Path(__file__)

def brew(url:str, raw:bool=False) -> BeautifulSoup|str:
    response = req.get(url)

    response.raise_for_status()

    document = response.text

    if raw:
        return document

    soup = BeautifulSoup(document, "html.parser")
    return soup

def get_vtuber_links(soup:BeautifulSoup) -> list:
    talent_list = soup.find(class_="talent_list clearfix")

    talent_links_list = [url.get("href") for url in talent_list.find_all("a")]

    return talent_links_list
    
def search_url(url:str) -> str:
    pattern = r".+/channel/(?P<id>.+)\?.+"

    match = re.search(pattern, url)

    if not match:
        meta_tags = brew(url).find_all("meta")

        for tag in meta_tags:
            content = tag.get("content")

            if not content:
                continue

            if "youtube" in content:
                match = re.search(pattern, content)

            if match:
                break

        if not match:
            raise Exception(f"Critical error: Could not find id for {url}. Content={content}")

    return match.group("id")

def get_channel_id(page:BeautifulSoup) -> str:
    talent_socials = page.find(class_="t_sns clearfix")
    channel_id = None

    for url in talent_socials.find_all("a"):
        if "youtube" in url.get("href"):
            channel_id = search_url(url.get("href"))
            break

    return channel_id

def get_talent_name(url:str) -> str:
    name = re.search(r".+talents/(?P<name>.+)/", url).group("name")

    name = name.strip().replace("-", " ").title()
    return name

def parse_talent_page(url:str) -> list[dict]:
    try:
        page = brew(url)
    except Exception as e:
        return {f"ERROR_FOR_{url}": "BAD_RESPONSE_PAGE"}

    name = get_talent_name(url)
    channel_id = get_channel_id(page)

    return {channel_id:{"name": name}}

def write_json(data:dict):
    with open(cwd / "data/hololive.json", "w") as file:
        json.dump(data, file, indent=4)

def main():
    talent_urls = []
    talent_data = {}

    print("Fetching https://hololive.hololivepro.com/en/talents ... ")
    soup = brew("https://hololive.hololivepro.com/en/talents")
    print("Successfully fetched https://hololive.hololivepro.com/en/talents")

    print("Getting Talent Urls...")
    talent_urls = get_vtuber_links(soup)
    print("Talent Urls Successfully Retrieved")

    for talent_url in progress(talent_urls, desc="Parsing talent data...", ncols=100, unit="pages"):
        talent_data.update(parse_talent_page(talent_url))
    print("Successfully parsed all talent pages")

    print("Writing to file...")
    write_json(talent_data)
    print("Successfully wrote to file")

    return talent_data

if __name__ == "__main__":
    main()