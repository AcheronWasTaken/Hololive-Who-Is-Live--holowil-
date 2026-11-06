# Holo-WhoIs-Live CLI Tool

## Description
This project is a super simple tool that tells you which hololive member is currently streaming. You can run it straight from your shell, and it will neatly print a table of all the hololive talents, and whether they are live or not. 

![alt-text](assets/Markdown/example.gif)

## Features
- Uses the Holodex API at https://holodex.net/api/v2 (Docs here: https://docs.holodex.net/#section/Holodex-API-Documentation) to get information on the talents, but does NOT use the available Holodex api wrapper at (https://github.com/ombe1229/holodex)
- Uses a scraper script that can be called on periodically to update information or when Hololive debuts a new gen. The script uses beautifulsoup4 and requests.
- Uses tabulate and tqdm to pretty print output, including progress bars.

## Installation Guide
1. Download the zip file in the releases section
2. Extract the zip
3. Run the exe :) (preferably via the cmd)

Alternatively, you can also use pipx to install it as CLI tool stored in your python directory:

1. Download the `.whl` file in the releases section.
2. Ensure you have `pipx` installed (globally) and that you have ran `pipx ensurepath` at least once. You can use `python -m pip install pipx` in a non-venv activated terminal to install it.
3. Run `pipx install <path to your wheel file>`
4. If everything ran smoothly, You can now run `holowil` from anywhere

## Usage
Since the project uses the Holodex API, you'll need your own API key. You can get one by heading over to "https://holodex.net/" --> click profile on the top right --> Log in/create account --> click "Account settings" --> Get new api key (if one isn't already shown to you).

You can either run `holowil --api-key=<your api key>` or use `holowil --config-api-key=<your api key>` and then simply just call `holowil`.

## Q&A

### If Holodex exists, why bother making this tool?
I don't know, Im bored I guess. This is just a tiny hobby project that I thought of to make randomly. I like having a lot of CLI tools on my computer that automates random things I didn't think I need to automate, and this project is just part of that, eventually, larger suite.

### How long will you maintain it?
Since i'll be using it myself, it'll be maintained for however long i will use it. Although any upcoming changes will most likely just be changes to the scraper in case Hololive changes their site.
