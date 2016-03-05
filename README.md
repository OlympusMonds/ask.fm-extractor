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
