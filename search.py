import json
import os
import string
from fuzzywuzzy import fuzz


TRANSCRIPT_FILE = os.path.join(os.getcwd(), "star_trek_master.json")

with open(TRANSCRIPT_FILE, "r", encoding="utf-8") as f:
    MASTER_DATA = json.load(f)

def normalize_line(line):
    """
    Cleans and standardizes a string for comparison.
    
    Lowercase the text, removes apostrophes (to handle contractions like "sky's" 
    as "skys"), removes leading/trailing punctuation from words, and collapses 
    multi-space gaps into single spaces.

    Args:
        line (str): The raw dialogue or search string to be cleaned.

    Returns:
        str: The normalized, lowercase, and space-joined string.
    """
    # split into words, strip punctuation and join together
    words = line.lower().replace("'", "").split()
    cleaned_words = [w.strip(string.punctuation) for w in words]
    return " ".join(cleaned_words)

def search_for_match(text=None, author=None, series=[None]):
    """
    Performs a direct substring search across the transcript master data.

    Iterates through the specified series and episodes to find lines where the 
    normalized search text exists within the normalized dialogue.

    Args:
        text (str, optional): The dialogue line to search. Defaults to None.
        author (str, optional): The name of the speaker to filter by. Defaults to None.
        series (list, optional): List of series keys (e.g., ['tos', 'tng']). Defaults to [None].

    Returns:
        list: A list of dictionaries containing match details, metadata, and surrounding context lines. Returns None if no text is provided.
    """
    if not isinstance(series, list): 
        series = [series]
    if text is None: 
        return None
    else: 
        text = normalize_line(text)

    matched_lines = []
    for series_name, episodes_list in MASTER_DATA.items():
        if series_name not in series:
            continue

        for i, episode in enumerate(episodes_list):
            for scene in episode:
                lines = scene.get("lines", [])

                for dialogue_i, dialogue_l in enumerate(lines):
                    try:
                        speaker = normalize_line(dialogue_l[0])
                        dialogue = normalize_line(dialogue_l[1])
                    except (IndexError, TypeError):
                        continue

                    if text in dialogue:
                        if author and normalize_line(author) != normalize_line(speaker):
                            continue
                        matched_lines.append(dict(
                            title=scene.get("title"),
                            season=scene.get("season"),
                            episode=scene.get("episode"),
                            speaker=dialogue_l[0],
                            lines_up=lines[max(0, dialogue_i-2):dialogue_i], # use max(0, ...) to ensure the slice starts at the beginning of the list if there aren't enough lines above
                            lines_down=lines[dialogue_i+1:dialogue_i+3],
                            match=" ".join(dialogue_l[1].split()), # remove double whitespaces
                            location=scene.get("location"),
                            dialogue_block_i=dialogue_i,
                            dialogue_line_i=i
                        ))

    return matched_lines

def search_for_partial_match(text=None, author=None, series=[None]):
    """
    Performs a fuzzy search using Levenshtein distance algorithms.

    Uses the fuzzywuzzy library to calculate the similarity between the search query and dialogue lines. 
    It checks 'ratio', 'token_set_ratio', and 'token_sort_ratio', taking the highest score.

    Args:
        text (str, optional): The search term. Defaults to None.
        author (str, optional): The name of the speaker to filter by. Defaults to None.
        series (list, optional): List of series keys (e.g., ['tos', 'tng']). Defaults to [None].

    Returns:
        list: A list of dictionaries for lines with a similarity score > 85. Includes a 'score' key representing the percentage of similarity.
    """
    if not isinstance(series, list): 
        series = [series]
    if text is None: 
        return None

    search_query = normalize_line(text)
    matched_lines = []
    best_score = 0
    best_match = None
    add_match = False

    for series_name, episodes_list in MASTER_DATA.items():
        if series_name not in series:
            continue

        for i, episode in enumerate(episodes_list):
            for scene in episode:
                lines = scene.get("lines", [])
                
                for dialogue_i, dialogue_l in enumerate(lines):
                    try:
                        speaker = normalize_line(dialogue_l[0])
                        dialogue = normalize_line(dialogue_l[1])
                    except (IndexError, TypeError):
                        continue

                    fuzzy_methods = [
                        lambda: fuzz.ratio(dialogue, search_query),
                        lambda: fuzz.token_set_ratio(dialogue, search_query),
                        lambda: fuzz.token_sort_ratio(dialogue, search_query)
                    ]
                    
                    p = 0 
                    for x in fuzzy_methods:
                        p = max(p, x())
                        if p > 85:# or add_match:
                            # Author filter
                            if author and normalize_line(author) != normalize_line(speaker):
                                continue

                            matched_lines.append(dict(
                                title=scene.get("title"),
                                season=scene.get("season"),
                                episode=scene.get("episode"),
                                speaker=dialogue_l[0],
                                lines_up=lines[max(0, dialogue_i-2):dialogue_i], # Context with safety max(0)
                                lines_down=lines[dialogue_i+1:dialogue_i+3],
                                match=" ".join(dialogue_l[1].split()), # remove double whitespaces
                                location=scene.get("location"),
                                dialogue_block_i=dialogue_i, # dialogue block index
                                dialogue_line_i=i, # dialogue line index
                                score=p # helpful for debugging fuzzy results
                            ))
                            break

    return matched_lines

if __name__ == "__main__":
    #search = input("Enter the keyword to search for > ")
    search = "spock"
    series = "tos"
    #series = input("series? > ")
    author = "kirk"

    matched_lines = search_for_match(search, author, [series])

    print (f"{len(matched_lines)} matches")

    for m in matched_lines:
        print (f"{m['title']} - Season: {m['season']} Episode: {m['episode']}, and we're in {m['location']}")
        print (f"{m['speaker']}: {m['match']}")

    print ("#########################################\n\n")

    if not matched_lines:
        print ("Searching using fuzzy wuzzy...")
        fuzz_lines = search_for_partial_match(search, author, series)

        for m in fuzz_lines:
            print (f"{m['title']} - Season: {m['season']} Episode: {m['episode']}, and we're in {m['location']}")
            print (f"{m['speaker']}: {m['match']}")
            print (f"Probability of match: {m['score']}%")