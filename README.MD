# Bannedwords

A simple Python script designed to review word documents (.docx and
.doc) and PDF files to identify any words that might be objectionable
to NIH policies.

The list of words is primarily taken from two sources:
* a list of NIH [disfavoured
words](https://www.nature.com/magazine-assets/d41586-026-01924-8/52836226),
as published in a June 26, 2026 [news article in
_Nature_](https://www.nature.com/articles/d41586-026-01924-8).
* an earlier list of words from a March 27, 2026 NY Times article [These Words Are Disappearing in the New Trump Administration](https://www.nytimes.com/interactive/2025/03/07/us/trump-federal-agencies-websites-words-dei.html).

Additional words in a similar spirit have been added as deemed appropriate.

# Installation

Requires a modern version of Python (I ran it on Python 3.14), with
two additional libraries:

* (pdfplumber 0.11.10](https://pypi.org/project/pdfplumber/)
* (python-docx 1.2.0 )[https://pypi.org/project/python-docx/))

See also the included `requirements.txt` for details.

# Usage

```
bannedwords --category_file <file> --directory <directory>
```

where

* `category_file` is the JSON file containing the banned words, in the
  format described below
* 'directory` is the directory containing the files to be scanned. All
  .doc, .docx, and .pdf files in that directory will be reviewed.

# Output

The output file will be a JSON blob keyed by the file name. Each file
name will have a dictionary keyed by the high-level categories found
in the `categories.json` (or equivalent) file. The dictionary for each
category will refer to a another dictionary, which will be contain the
words assocaited with that category. The value associated for that
word will be an instance of occurrences of that word in the
document. Each occurrence will take the form of a tuple containing the
index of the paragraph (starting from 0) and the text of the paragraph.

# Banned wordlist

The banned wordlist is found in the `categories.json` file. This file
contains a dictionary keyed of of several broad categories: Climate
change, DEI, Gender, Misinformation, and Vaccine Hesitancy.  Each of
those keys has a list of words associated with it.

This words included in this list is a slightly modified version of the 
[list](https://www.nature.com/magazine-assets/d41586-026-01924-8/52836226),
published by Nature on June 26, 2026 (included in the bannedwords.pdf
file). Some words have been added to avoid possible false
negatives. For example, although `workforce diversification` was
included in the published file, `diversification` was not. The
`categories.json` file can be adapted as needed. 
