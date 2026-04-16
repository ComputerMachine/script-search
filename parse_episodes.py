import os
import json
import re
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag


# Configuration
TRANSCRIPT_DIR = 'transcripts'
OUTPUT_FILE = 'star_trek_master.json'

def parse_transcripts():
    master_data = {
        "tos": [],
        "tng": [],
        "ds9": [],
        "voy": [],
        "ent": [],
        "tas": []
    }

    for series in os.listdir(TRANSCRIPT_DIR):
        for filename in os.listdir(os.path.join(TRANSCRIPT_DIR, series)):
            if not filename.endswith('.htm'):
                continue

            filepath = os.path.join(TRANSCRIPT_DIR, series, filename)

            with open(filepath, "r", encoding="latin-1") as f:
                soup = BeautifulSoup(f.read(), "html.parser")
                scenes = []
                try:
                    scene_locations = [scene for scene in soup.find("table").find_all("b")]
                except AttributeError:
                    raise Exception("Table was not found in data passed to BeautifulSoup, was the raw transcript file downloaded properly?")

                meta = {
                    "title": soup.find("span", {"id": "name"})["value"],
                    "season": soup.find("span", {"id": "season"})["value"],
                    "episode": soup.find("span", {"id": "episode"})["value"]
                }

                print ("Working on {}...".format(meta.get("title")))

                for stage in scene_locations:
                    stage_name = stage.text.strip("[]")
                    dialogue_p = stage.find_next("p") # target the paragraph containing the dialogue

                    if not dialogue_p:
                        continue

                    normalized_lines = []
                    for line in dialogue_p.stripped_strings:
                        if ":" in line:
                            normalized_lines.append(line.replace("\n", " ").split(":", 1))
                    
                    scenes.append({
                        **meta,
                        "location": stage_name,
                        "lines": normalized_lines
                    })

                master_data[series].append(scenes)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        print ("Writing data to json file...")
        json.dump(master_data, f, indent=2)

    print(f"\nSuccess! Consolidated JSON created at: {OUTPUT_FILE}")

if __name__ == "__main__":
    parse_transcripts()
    exit()
    
    # testing 
    INPUT_FILE = os.path.join(os.getcwd(), OUTPUT_FILE)
    with open(INPUT_FILE, "r") as f:
        data = json.loads(f.read())

    for series in data:
        print (series)

    for series in data:
        for episode in data[series]:
            print (series, episode.keys())


    #parse_transcripts()