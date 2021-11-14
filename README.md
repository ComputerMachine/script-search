# Star Trek Script Search
A tool created to replace the almighty star trek script search previously at scriptsearch.dxdy.name

# Bugs
* When downloading transcripts, some episodes for two parters are in one file, and for the 2nd part just uses a html redirect to an html ID (ex: 
`Transcript file already exists for /voy/: 525.htm ... Skipping
Downloading voy transcript from http://www.chakoteya.net/Voyager/525.htm#To%20Be%20Continued..` )
* When searching for an phrase or word, it may come back with an incorrect episode number. Two part episodes are sometimes contained in a single file, therefore if the word or phrase appears anywhere in that file, it will give the same episode number. (ex: Picard tells Q to 'Get off my ship' in Encounter at Farpoint, which is stored as episode 1, but because it is a two parter, it is technically episode 2.)
* line 88 of `get_episodes_and_parse.py` will get every line except for the last one, obviously the goal is to be able to search every single word spoken.

# HOW TO USE
* Install dependencies (BeautifulSoup)
* run `python download_transcripts.py` to fetch raw transcript files from chakoteya.net
* `python parse_episodes.py` to convert those raw transcript files into some beautiful json
* `python search.py` and it will prompt you for your word or phrase

# Trying to make sense of this download episodes algorithm
1. Get URL's for every episode in a given series.
2. Check if series directory exists, if not, create it.
3. Iterate through every season
    * Iterate through every episode in given season
        * If exists, skip it.
    * Download remote file with given URL and save to raw transcript folder
    * Open that file, insert tag with specific identifers, such as season #, episode #, etc that we couldn't get anywhere else