import requests as re
import click
from scraper import main as make_json
from pathlib import Path
import json
from tqdm import tqdm as progress
from tabulate import tabulate
from termcolor import colored

class Talent:
    def __init__(self, name:str, channel_id:str):
        self.name = name
        self.channel_id = channel_id
        self.status = False
        self.checked = False

def get_api_key():
    with open("data/api_key.key", "r") as file:
        return file.read()

def get_data() -> dict[str, dict]:
    if Path("data/hololive.json").exists:
        with open("data/hololive.json", "r") as file:
            return json.load(file)

    print("Could not find data/hololive.json. Making json fike...")
    return make_json()
    
def get_videos(api:str, channel_ids:list) -> list[dict]:
    payload = {"channels": ",".join(channel_ids)}
    headers = {"X-APIKEY": api}

    response = re.get("https://holodex.net/api/v2/users/live", params=payload, headers=headers)

    response.raise_for_status()

    return response.json()

@click.command()
def main():
    api_key = get_api_key()
    talents = get_data()
    channel_ids = []
    checked_talents = 0

    for channel_id in talents:
        talents[channel_id].update({
            "object": Talent(
                name=talents[channel_id]["name"],
                channel_id=channel_id,
            )
        })

        channel_ids.append(channel_id)

    for video in progress(get_videos(api=api_key, channel_ids=channel_ids), desc="Checking through received videos", unit="videos", ncols=150):
        channel_id = video.get("channel_id") or video.get("channel").get("id")

        if not channel_id:
            raise Exception(f"Channel ID not found: {video}")

        try:
            talent:Talent = talents[channel_id]["object"]
        except KeyError:
            continue

        status = video.get("status")

        if talent.checked:
            continue

        if status == "live":
            talent.status = True
            talent.checked = True
            checked_talents += 1

        if checked_talents == len(talents):
            break

    table = []
    for channel_id in talents:
        talent = talents[channel_id]["object"]

        table.append({"Name": talent.name, "Channel Id": talent.channel_id, "Status": colored("Live", "green") if talent.status else colored("Not Live", "red")})

    print(tabulate(table))
        
if __name__ == "__main__":
    main()

    



