import json
import os


if __name__ == "__main__":
    parent = "json_transcripts\\tng\\"
    files = os.listdir(parent)
    data_files = []

    for file in files:
        with open(parent + file) as f:
            data_files.append(json.load(f))

    search_line = input("Enter the keyword to search for > ")

    import string

    for data in data_files:
        for scene_number in data:
            for scene_location in data[scene_number]:
                for dialogue_line in data[scene_number][scene_location]:
                    try:
                        speaker = dialogue_line[0]
                        line = dialogue_line[1]
                    except IndexError: # this dialogue_line is a description of whats happening in the scene, no speaker
                        continue
                    normalized_line = line.lower()
                    normalized_line = normalized_line.translate(str.maketrans('', '', string.punctuation))
                    if search_line.lower() in normalized_line:
                        episode_name = data["0"]["title"]
                        season = data["0"]["season"]
                        episode = data["0"]["episode"]

                        print ("Season {}, Episode, {}, [{}]: {}".format(season, episode, episode_name, line))