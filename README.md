# Star Trek Script Search
Search for any word or phrase spoken in Star Trek: TNG, DS9, Voyager, Enterprise, TOS. A wide variety of filters are also available.

A tool created to replace the almighty star trek script search previously at scriptsearch.dxdy.name

# How to use
You should already have the formatted transcript files, if not:

    pip install -r requirements.txt    
    python download_transcripts.py

and it will attempt to fetch the raw transcripts from chakoteya.net

Next, run `parse_episodes.py` to convert them into json files.

Execute `search.py` and search for the word or phrase you were thinking of!

# Bugs
* When downloading transcripts, some episodes for two parters are in one file, and for the 2nd part just uses a html redirect to an html ID (ex: 
`Transcript file already exists for /voy/: 525.htm ... Skipping
Downloading voy transcript from http://www.chakoteya.net/Voyager/525.htm#To%20Be%20Continued..` )
* When searching for an phrase or word, it may come back with an incorrect episode number. Two part episodes are sometimes contained in a single file, therefore if the word or phrase appears anywhere in that file, it will give the same episode number. (ex: Picard tells Q to 'Get off my ship' in Encounter at Farpoint, which is stored as episode 1, but because it is a two parter, it is technically episode 2.)
* line 88 of `get_episodes_and_parse.py` will get every line except for the last one, obviously the goal is to be able to search every single word spoken.