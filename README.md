
<p align="center">
  <img src="res/obsidian_logo.png" alt="Obsidian Logo" width="200"/>
</p>


# Obsidian Tools

This repository contains tools to help manage an [Obsidian](https://obsidian.md/) vault.


## Installation

Install UV
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Clone the repo
```bash
git clone git@github.com:FredCarvalhoOliveira/obsidian-tools.git 
cd obsidian-tools
```

Install dependencies
```bash
uv sync
```




## `find_links.py`

This Python script helps you find potential links between your notes that you might have missed.

### What it does

The script scans all your markdown files in the specified vault directory. If it finds a piece of text that matches the filename of another note (without the `.md` extension), it will ask you if you want to convert it into a proper `[[wikilink]]`.

This is useful for quickly creating connections between your notes and building a more networked knowledge base.




### How to use
1.  Run the script with the path to your Obsidian vault as an argument:
    ```bash
    uv run find_links.py /path/to/your/vault
    ```
2.  The script will show you potential links one by one and ask for your confirmation before making any changes.
