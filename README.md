# Filter-translate

This is a tool to google-translate a text file except for the lines you filter out specifically -- leave them untranslated.

```shell
usage: filter-translate.py [-h] [--version] [--filter= FILTER] [-s SOURCE_LANGUAGE] [-t TARGET_LANGUAGE] [--encoding ENCODING] infile outfile

options:
  -h, --help            show this help message and exit
  --version             show program version number and exit
  --filter= FILTER      Prefix filter with + or -. Translate only lines that +do or -do not match regex. e.g.
                        --filter='+(^//)|(^#)'
  -s SOURCE_LANGUAGE, --source_language SOURCE_LANGUAGE
                        Source language (2-letter ISO639-2 codes); default=nl
  -t TARGET_LANGUAGE, --target_language TARGET_LANGUAGE
                        Target language (2-letter ISO639-2 codes); default=en
  --encoding ENCODING   Character encoding used to interpret the in/out files; default=utf-8

If you need a more clever filter than regex then you will need to write a filter function based on the regex example filter in this program.
```

## Installation

It is necessary to set up a google cloud translate account. It's payware but the give you something like a gigabyte free:

1. Set up google cloud translate. It involves several steps that you've got to get right: [described here](https://cloud.google.com/translate/docs/setup).
2. pip install --upgrade google-cloud-translate

