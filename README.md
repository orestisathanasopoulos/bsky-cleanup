# bsky-cleanup


I had to deal with a compromised Bluesky account recently that had a lot of junk posts to clean up so I used this script to automate the process and I'm putting it out there in case other people can find it useful.

It's fairly easy to use:

1. Set up a python virtual environment (optional but recommended)
    e.g. `pyenv virtualenv bsky`

2. Install requests
   `pip install requests` or `python3 -m pip install requests`

3. Run the script
   `python bsky.py` or `python3 bsky.py`
