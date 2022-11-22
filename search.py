import json
import os
import string


def normalize_line(line):
    return line.lower().translate(str.maketrans('', '', string.punctuation))#.replace(" ", "")

def search_for_match(text=None, author=None, series=[None]):
    if type(series) != list: series = [series]
    if text is None: 
        return None
    data_files = []
    matched_lines = []
    folders = {
        "tng": "json_transcripts\\tng\\",
        "ds9": "json_transcripts\\ds9\\",
        "voy": "json_transcripts\\voy\\",
        "tos": "json_transcripts\\tos\\",
        "tas": "json_transcripts\\tas\\",
        "ent": "json_transcripts\\ent\\"
    }
    for s in series:
        if folders.get(s) is None:
            continue
        files = os.listdir(folders.get(s))
        data_files = []

        for file in files:
            with open(folders.get(s) + file) as f:
                data_files.append(json.load(f))

        for i, data_segment in enumerate(data_files): # a list of json objects
            for scene_number in data_segment: # every data segment is organized by scene numbers
                for scene_location in data_segment[scene_number]: # iterate through every scene location, which the dialogue is stored under
                    for dialogue_index, dialogue_line in enumerate(data_segment[scene_number][scene_location]):
                        try:
                            speaker = dialogue_line[0]
                            normalized_line = normalize_line(dialogue_line[1])
                            normalized_search = normalize_line(text.lower())
                        except IndexError:
                            # this dialogue_line is a description of whats happening in the scene, no speaker
                            continue

                        if normalized_search in normalized_line:
                            matched_line = dialogue_line[1]
                            up = data_segment[scene_number][scene_location][dialogue_index-2:dialogue_index] # 2 dialogue lines from before the matched line
                            down = data_segment[scene_number][scene_location][dialogue_index+1:dialogue_index+3] # 2 dialogue lines after the matched line
                            matched_lines.append(dict(
                                title=data_segment["0"]["title"],
                                season=data_segment["0"]["season"],
                                episode=data_segment["0"]["episode"],
                                speaker=speaker,
                                lines_up=up,
                                lines_down=down,
                                match=matched_line,
                                scene_location=scene_location,
                                scene_number=scene_number,
                                data_segment_index=i
                            ))
    return matched_lines


if __name__ == "__main__":
    search = input("Enter the keyword to search for > ")
    series = "tos"
    author = None
    matched_lines = search_for_match(search, author, series)

    print ("{} matches".format(len(matched_lines)))

    for m in matched_lines:
        print ("Season {} Episode {} and we're in {}".format(
            m.get("season"),
            m.get("episode"),
            m.get("scene_location")
        ))
        print ("({episode}) {speaker}: {line}".format(
            episode=m.get("title"), 
            speaker=m.get("speaker"), 
            line=m.get("match"))
        )
        print ("#########################################\n\n")