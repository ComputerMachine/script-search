import json
import re
import os

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag


def normalize(data):
    try:
        speaker, line = data.replace("\n\n", " ").replace("\n", " ").split(":")
    except ValueError:
        # scene description, just pass this back
        return data.replace("\n\n", " ").replace("\n", " ").strip()

    speaker = speaker.lstrip()
    line = line.lstrip().rstrip()
    return speaker, line

def convert_to_json_file(series):
    transcript_folder = os.getcwd() + "/transcripts"
    if series == "tng":   series_folder = "/tng/"
    elif series == "ds9": series_folder = "/ds9/"
    elif series == "voy": series_folder = "/voy/"
    elif series == "tos": series_folder = "/tos/"
    elif series == "ent": series_folder = "/ent/"
    elif series == "tas": series_folder = "/tas/"

    try:
        files = os.listdir(transcript_folder + series_folder)
    except FileNotFoundError:
        raise FileNotFoundError("You need to download the raw transcripts first. There's nothing in the folder to parse!")

    for file in files:
        fpath = transcript_folder + series_folder + file
        new_file_folder = os.getcwd() + "/json_transcripts" + series_folder
        new_file_path = new_file_folder + file.split(".")[0] + ".json"

        if not os.path.exists(os.getcwd() + "/json_transcripts"):
            print ("Creating JSON Transcript folder...")
            os.makedirs(os.getcwd() + "/json_transcripts")
        if not os.path.exists(new_file_folder):
            print ("Creating {} directory...".format(series))
            os.makedirs(new_file_folder)
        if os.path.exists(new_file_path):
            print ("Parsed transcript file already exists for {} {}, skipping...".format(series, file))
            continue

        with open(fpath, encoding="latin-1") as f:
            rdata = f.read()

        print ("Parsing {} {} file...".format(series, file))
        data = parse_transcript_file(rdata)

        with open(new_file_path, "w") as fp:
            json.dump(data, fp)

    print ("Series {} completed.".format(series))

def parse_transcript_file(data):
    """Take a raw transcript file and return speaker blocks"""
    soup = BeautifulSoup(data, "html.parser")
    
    try:
        scene_locations = [scene for scene in soup.find("table").find_all("b")]
    except AttributeError:
        raise Exception("Table was not found in data passed to BeautifulSoup, was the raw transcript file downloaded properly? Try redownloading it.")
    
    # scene number, followed by the scene location, and then a list with speaker at 0, dialogue at 1
    scenes = {s:[] for s in range(len(scene_locations))}
    for n, stage in enumerate(scene_locations):
        stage_name = stage.text.strip("[").strip("]")

        # dialogue block is in the p tag, every line is seperated by a br tag
        dialogue_lines = [
            line.previous_sibling for line in stage
                .find_next("p") # NOTE: will not get the last line of every transcript!
                .find_all("br")
        ]

        normalized_lines = [
            line
            .strip()
            .replace("\n", " ")
            .split(":")
            for line in dialogue_lines if isinstance(line, NavigableString)
        ]
        scenes[n] = {
            "title": soup.find("span", {"id": "name"})["value"],
            "season": soup.find("span", {"id": "season"})["value"],
            "episode": soup.find("span", {"id": "episode"})["value"],
            stage_name: normalized_lines
        }

    return scenes

def parse_transcript_file_old(data):
    soup = BeautifulSoup(data, "html.parser")

    try:
        scene_locations = [scene for scene in soup.find("table").find_all("b")]
    except AttributeError:
        raise Exception("Table was not found in data passed to BeautifulSoup, was the raw transcript file downloaded properly? Try redownloading it.")

    tags = soup.find("table").find("td").descendants

    counter = 0
    scenes = []
    scene_counter = 0
    current_scene = []
    dialogues = []
    in_scene_now = False

    for tag in tags:
        if tag.name == "b": # new location scene
            scene_location = tag.get_text().replace("\n\n", " ")
            in_scene_now = True
            print ("Location found: ", scene_location)

        if in_scene_now:
            if isinstance(tag, NavigableString):
                if tag.next_element.name == "b":
                    # this dialogue block has ended
                    in_scene_now = False
                    line = tag.string.replace("\n\n", " ").lstrip()
                    dialogues.append(line)
                    scenes.append({scene_location: dialogues})
                    dialouges = []
                    continue
                line = tag.string.replace("\n\n", " ").lstrip()
                dialogues.append(line)
            
            if isinstance(tag, Tag):
                if tag.name != "b":
                    print ("type: ", type(tag.next_sibling), tag.next_sibling.get_text())
                    print ("sib:", dir(tag.next_sibling))
                    if tag.next_sibling is None:
                        continue
                    line = tag.next_sibling.get_text().replace("\n\n", " ").lstrip()
                    dialogues.append(line)

        counter += 1
        if counter >= 100:
            break

    print (scenes)
    return scenes


if __name__ == "__main__":
    print ("Converting all raw transcript files into json...")
    series = os.listdir(os.getcwd() + "/transcripts")
    for s in series:
        convert_to_json_file(s)