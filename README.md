# Star Trek Script Search

A command-line tool to search through Star Trek episode transcripts (TOS, TNG, DS9, Voyager, Enterprise) for any word or phrase -- with flexible filtering and fast local lookup.

## 🚀 Features

- Search lines from all major Star Trek series --
\n- Supports word and phrase search --
\n- Filter by series, season, episode, character --
- Automated transcript downloading --
- Fast local searching using JSON files 

## 📦 Getting Started

**Prerequisites**

- Python 3.x

**Installation**

1. Clone the repository:

```bash
git clone https://github.com/ComputerMachine/script-search.git
cd script-search
```


2. Install requirements:

```bash
pip install -r requirements.txt
```

**Optional**

a. If you need to redownload the raw transcripts:

```bash
python download_transcripts.py
```


b. Parse transcripts into JSON:

```bash
python parse_episodes.py
```

## 🔍 Usage

Run the search tool:

```bash
python search.py
```

You'll be prompted to enter a word or phrase.

Optional filters include:
- Series (TNG, DSY, VOY, etc.)
- Season
- Episode
- Character

Example input:

live long and prosper

## ⚠️ Known Issues 

- Some two-part episodes are merged into a single transcript file --
- Episode numbers may appear incorrect for multi-part episodes
- The parser may skip the final line of certain transcripts
- It's been awhile since I've touched this project, just scan it for efficiency and make sure that the JSON is all in one file, no point in it being in multiple

## 💡 Why This Project?

This tool was created as a modern, local, and scriptable replacement for scriptsearch.dxdy.name, enabling fast offline full-text searching of Star Trek transcripts.

## 📙 Future Ideas

- Web-based search UI 
- Use ML or AI
- Support for newer series (Discovery, Picard, SNW)
- Fuzzy / approximate search
- Statistics (character usage, phrase frequency)
- Export search results to CSV or Markdown 

## 📚 License & Credits

- **License** See the LICENSE file for full details.
- **Transcript Source:** chakoteya.net
- **Author:** ComputerMachine

