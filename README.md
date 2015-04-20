## Haiku Generator

The main haiku generation code is in `experiment.py`
Content generation using Word Association Networks (WAN) is in `wan.py`
Content generation using WordNet is in `word_net_util.py`
Scraping/haiku collection code is in `crawl.py`

Other files contain utility functions used in the main modules or some experiments we did (like using bigrams for everything) before we found the optimal method to generate haiku.

# Dependencies

To resolve dependencies, please run:
`sudo pip install -r requirements.txt`

If you get an issue with a python import related to nltk, please run `sudo python -m nltk.downloader -d /usr/share/nltk_data all`
