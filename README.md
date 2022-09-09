# Filter-translate

This is a tool to google-translate a text file except for the lines you filter out specifically -- leave them untranslated.

I built it to translate source code files that had heaps of comments from Dutch to English.

```shell
usage: filter-translate.py [-h] [--version] [--filter= FILTER] [-s SOURCE_LANGUAGE] [-t TARGET_LANGUAGE] [--encoding ENCODING] infile outfile

options:
  -h, --help            show this help message and exit
  --version             show program version number and exit
  --filter=FILTER       Prefix filter with + or -. Translate only lines that +do or -do not match regex. e.g.
                        --filter='+(^//)|(^#)'
  -s SOURCE_LANGUAGE, --source_language SOURCE_LANGUAGE
                        Source language (2-letter ISO639-2 codes); default=nl
  -t TARGET_LANGUAGE, --target_language TARGET_LANGUAGE
                        Target language (2-letter ISO639-2 codes); default=en
  --encoding ENCODING   Character encoding used to interpret the in/out files; default=utf-8

If you need a more clever filter than regex then you will need to write a filter function based on the regex example filter in this program.
```

## Installation

It is necessary to set up a google cloud translate account. It's payware but they give you half a gigabyte per month for free, so you can do plenty of translations for free:

1. Set up google cloud translate. It involves several steps that you've got to get right: [described here](https://cloud.google.com/translate/docs/setup).
2. Set environment variable GOOGLE_APPLICATION_CREDENTIALS to point to your cred.json file that you downloaded in step 1.
3. Run `pip install --upgrade google-cloud-translate`

## Run it

`python filter-translate.py --help`

Also take a look at `example.sh` to show you how to translate a whole tree of selected files.
