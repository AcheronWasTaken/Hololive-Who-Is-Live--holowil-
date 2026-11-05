import requests as re
import click

def get_api_key():
    with open("data/api_key.key", "r") as file:
        return file.read()

def get_channels(api:str):
    payload = {"org": "Hololive"}
    headers = {"X-APIKEY": api}


    response = re.get("https://holodex.net/api/v2/channels", params=payload, headers=headers)

    response.raise_for_status()

    return response.json()

@click.command()
def main():
    key = get_api_key()

    channels = get_channels(key)

    for channel in channels:
        if channel["type"] == "vtuber":
            print(f"{channel["name"]} is {"not live" if channel["inactive"] else "live"}")

if __name__ == "__main__":
    main()

    



