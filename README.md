# SWRPG Dice Discord Bot
## About
This is a collection of code for running a discord bot capable of rolling the narrative dice used in [Fantasy Flight's Star Wars RPG](https://www.fantasyflightgames.com/en/starwarsrpg/).
## File Manifest
Below is a map of all of the files contained in the repository:
```
SWRPG Dice Discord Bot
├── API_KEY
├── AUTHORS.tsv
├── content
│   ├── emoji_assets
│   │   └── (...)
│   └── text_summaries.yml
├── CONTRIBUTING.md
├── environment.yml
├── LICENSE.md
├── main.py
├── README.md *
└── src
    ├── dice.py
    └── emoji.py
```
And a list of highlights from the map:
- **API_KEY**: add this file yourself; it should contain your Discord API key on the first line. See [setup](#setup) for more details.
- **content/emoji_assets**: symbols for narrative dice. These were ripped from the fonts in official PDFs of Edge of the Empire and then recolored. They are therefore as close a recreation of the symbols as possible.
- **content/text_summaries.yml**: text summaries used for the first line in the bot's responses. More can be added if desired.
- **environment.yml**: conda-readable description of the project environment. See [setup](#setup) for more details.
- **main.py**: entry point for starting the bot.

## Setup
To get started, clone the repository with **git clone** into a directory of your choice:
> git clone https://github.com/Ezuharad/SWRPG-Dice-Discord-Bot \<path/to/project>

After this you will need to create a [conda environment](https://docs.conda.io/en/latest/) for the project using **environment.yml**:
> conda env create --name \<your environment name> --file=environment.yml

Finally, create the file **API_KEY** in the root directory of the project and put your [Discord API key](https://discord.com/developers/docs/reference) in the first line.

Optionally, if you want to add emoji to your instance of the bot, you will need to upload the assets you want from **content/emoji_assets** to your discord server, then replace the contents of **src/emoji.py** with the IDs for your server.
