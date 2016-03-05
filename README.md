# ask.fm extractor

The ask.fm website is a great way to get long-form answers from people on the internet.
Unfortunately, the website is not super conducive to going through (or searching for) older answers.

This script extracts all questions and answers from a particular account into a very basic format. Oldest to newest (except the latest page), question, answer, delimiting text.

Usage:
```
python extract.py <account-name> 
```

For example:
```
python extract.py OlympusMonds > monds.txt  # redirecting to a file is a good idea
```

I imagine if you go too hard on this, ask.fm may get annoyed, so take it easy.

# TODO:
- Make it get the latest page
- Check how old the pickle file is (or maybe only have it for debug mode?)
