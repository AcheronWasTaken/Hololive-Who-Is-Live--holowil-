import requests as re
import click
from .scraper import main as make_json
from pathlib import Path
import json
from tqdm import tqdm as progress
from tabulate import tabulate
from termcolor import colored

cwd = Path(__file__).parent

class Talent:
    def __init__(self, name:str, channel_id:str):
        self.name = name
        self.channel_id = channel_id
        self.status = False
        self.checked = False

def get_api_key():
    if Path(cwd / "data/api_key.key").exists():
        with open(cwd / "data/api_key.key", "r") as file:
            key = file.read()

            if not key:
                raise click.ClickException("API key file is empty. Please run 'holowil --config-api-key=<your key>' or supply it with '--api-key=<your-api-key>'")

            return key  
        
    raise click.ClickException("API key file not found. Please run 'holowil --config-api-key=<your key>' or supply it with '--api-key=<your-api-key>'")

def put_api_key(api_key:str):
    Path(cwd / "data").mkdir(exist_ok=True)
    with open(cwd / "data/api_key.key", "w") as file:
        file.write(api_key)
        
def get_data() -> dict[str, dict]:
    if Path(cwd / "data/hololive.json").exists():
        with open(cwd / "data/hololive.json", "r") as file:
            data = json.load(file)

            if data:
                return data

    print("Could not find data/hololive.json. Making json file...")
    return make_json()
    
def get_videos(api:str, channel_ids:list) -> list[dict]:
    payload = {"channels": ",".join(channel_ids)}
    headers = {"X-APIKEY": api}

    response = re.get("https://holodex.net/api/v2/users/live", params=payload, headers=headers)

    try:
        response.raise_for_status()
    except Exception as e:
        raise click.ClickException(f"Bad Response: {e}"[:70] + "...")

    return response.json()

@click.command(name="holowil")
@click.option("--api-key", default=None, help="Manually supply your own api key if you'd like to use a different one, or the file is not working.")
@click.option("--config-api-key", default=None, help="Save your key to the api_key.key file for later usage")
def cli(api_key:str, config_api_key:str):
    """CLI tool to get data on which hololive talent is currently streaming (Who is live?)"""

    if config_api_key:
        put_api_key(config_api_key)
        print("Successfully wrote key to data/api_key.key.")
        return

    api_key = api_key or get_api_key()
    talents = get_data()
    channel_ids = []
    checked_talents = 0

    for channel_id in talents:
        if "ERROR_FOR_" in channel_id:
            continue

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
            continue

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

    print(tabulate(table, headers="keys"))
        
if __name__ == "__main__":
    cli()

    



