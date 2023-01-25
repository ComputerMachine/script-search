import json
import os
import string
from fuzzywuzzy import fuzz


def normalize_line(line):
    return line.lower().translate(str.maketrans('', '', string.punctuation))#.replace(" ", "")

def sort_matched_data(dialogue_line, data_segment, text):
    speaker = dialogue_line[0]
    matched_line = dialogue_line[1]
    return dict(
        title=data_segment["0"]["title"],
        season=data_segment["0"]["season"],
        episode=data_segment["0"]["episode"],
        speaker=speaker,
        match=matched_line
    )

def search_for_partial_match(text=None, author=None, series=[None]):
    if type(series) != list: series = [series]
    if text is None: 
        return None
    data_files = []
    matched_lines = []
    folders = {
        "tng": "json_transcripts/tng/",
        "ds9": "json_transcripts/ds9/",
        "voy": "json_transcripts/voy/",
        "tos": "json_transcripts/tos/",
        "tas": "json_transcripts/tas/",
        "ent": "json_transcripts/ent/"
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

    if len(matched_lines) == 0:
        print ("No direct line matches, using fuzzywuzzy...")
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

                        p = fuzz.ratio(normalize_line(dialogue_line[1]), text.lower())
                        if p > 80:
                            matched_line = dialogue_line[1]
                            sorted_data = sort_matched_data(dialogue_line, data_segment, text)
                            matched_lines.append(dict(
                                sorted_data,
                                lines_up=data_segment[scene_number][scene_location][dialogue_index-2:dialogue_index], # 2 dialogue lines from before the matched line,
                                lines_down=data_segment[scene_number][scene_location][dialogue_index+1:dialogue_index+3], # 2 dialogue lines after the matched line,
                                scene_location=scene_location,
                                scene_number=scene_number,
                                data_segment_index=i
                            ))

    if len(matched_lines) == 0:
        print ("Couldn't find matched lines from fuzzywuzzy token sort, break up the string and try again.")
        for i, data_segment in enumerate(data_files): # a list of json objects
            for scene_number in data_segment: # every data segment is organized by scene numbers
                for scene_location in data_segment[scene_number]: # iterate through every scene location, which the dialogue is stored under
                    for dialogue_index, dialogue_line in enumerate(data_segment[scene_number][scene_location]):
                        try:
                            speaker = dialogue_line[0]
                            transcript_line = dialogue_line[1].lower()
                            search_line = text.lower()
                        except IndexError:
                            # this dialogue_line is a description of whats happening in the scene, no speaker
                            continue

                        words = search_line.split(" ")

                        for x in range(len(words)):
                            joined = " ".join(words)
                            #print ("Search value: ", joined)
                            #print ("Against: ", transcript_line)
                            p = fuzz.token_sort_ratio(joined, transcript_line)
                            if p > 80:
                                matched_line = dialogue_line[1]
                                sorted_data = sort_matched_data(dialogue_line, data_segment, text)
                                matched_lines.append(dict(
                                    sorted_data,
                                    lines_up=data_segment[scene_number][scene_location][dialogue_index-2:dialogue_index], # 2 dialogue lines from before the matched line,
                                    lines_down=data_segment[scene_number][scene_location][dialogue_index+1:dialogue_index+3], # 2 dialogue lines after the matched line,
                                    scene_location=scene_location,
                                    scene_number=scene_number,
                                    data_segment_index=i
                                ))
                                break
                            words.pop(0)

    return matched_lines



def search_for_match(text=None, author=None, series=[None]):
    if type(series) != list: series = [series]
    if text is None: 
        return None
    data_files = []
    matched_lines = []
    folders = {
        "tng": "json_transcripts/tng/",
        "ds9": "json_transcripts/ds9/",
        "voy": "json_transcripts/voy/",
        "tos": "json_transcripts/tos/",
        "tas": "json_transcripts/tas/",
        "ent": "json_transcripts/ent/"
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
    series = input("series? > ")
    author = None
    matched_lines = search_for_partial_match(search, author, series)

    print ("{} matches".format(len(matched_lines)))

    print (matched_lines)

    for m in matched_lines:
        print (m.get("match"))

    #for m in matched_lines:
    #    break
   #     print ("Season {} Episode {} and we're in {}".format(
    #        m.get("season"),
    #        m.get("episode"),
    #        m.get("scene_location")
    #    ))
     #   print ("({episode}) {speaker}: {line}".format(
    #        episode=m.get("title"), 
     #       speaker=m.get("speaker"), 
    #        line=m.get("match"))
    #    )
   #     print ("#########################################\n\n")