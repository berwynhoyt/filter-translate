#!/usr/bin/env python3
# Translate a files using google cloud translate API v3 (Advanced)

# It is necessary to set up your google cloud account as described here:
#  https://cloud.google.com/translate/docs/setup
# And run: pip install --upgrade google-cloud-translate

Charlimit = 30720   # a google limit on chars per request

import sys
import os
import json
import re

from google.cloud import translate

class TranslationError: pass

Keep_incomplete_files = False       # for debugging

class Translator:
    def __init__(self, in_lang='nl', out_lang='en', line_filter=None, encoding='utf-8', filter_data=None, project_id=None):
        """ Init translator
            If function line_filter(line, filter_data) is supplied then translation will pass it
            every line and it must return True to keep that line untranslated.
            filter_data is always passed to line_filter verbatim.
        """
        self.in_lang = in_lang
        self.out_lang = out_lang
        self.line_filter = line_filter
        self.filter_data = filter_data
        self.encoding = encoding

        if not project_id:
            credentials_file = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
            if credentials_file is None:
                raise TranslationError("Environment variable GOOGLE_APPLICATION_CREDENTIALS must point to your cred.json file. Follow setup instructions at https://cloud.google.com/translate/docs/setup")
            with open(credentials_file) as f:
                google_data = json.load(f)
            project_id = google_data['project_id']
        self.project_id = project_id


    def translate_text(self, text="YOUR_TEXT_TO_TRANSLATE"):
        """ Translate text which is a str or list of strings.
            Maximum characters in one request is Charlimit.
            Return list of strings
        """
        if type(text) == str:
            text = [text]

        location = "global"
        parent = f"projects/{self.project_id}/locations/{location}"
        client = translate.TranslationServiceClient()

        response = client.translate_text(
            request={
                "parent": parent,
                "contents": text,
                "mime_type": "text/plain",  # mime types: text/plain, text/html
                "source_language_code": self.in_lang,
                "target_language_code": self.out_lang,
            }
        )
        if 'translations' not in response:
            raise TranslationError("Error getting the data from google translate API")
        strings = [s.translated_text for s in response.translations]
        return strings


    def translate_lines(self, lines, output_lines=None):
        """ Translate list of lines in chunks <Charlimit chars, ensuring we split at a line break.
            Skip translation of lines flagged by self.line_filter.
            Append lines to output_lines list and return it.
        """
        def merge_translation(to_translate, not_translate, output_lines):
            """ Translate and merge translated and non-translated lines """
            translated = self.translate_text(to_translate)
            for l in not_translate:
                if l is None:
                    output_lines.append(translated.pop(0))
                else:
                    output_lines.append(l)

        if output_lines is None:
            output_lines = []
        to_translate = []
        not_translate = []
        buffered_length = 0
        line_number = 0
        for line in lines:
            line_number += 1
            if self.line_filter and self.line_filter(line, self.filter_data):
                not_translate.append(line)
                continue
            if len(line) >= Charlimit:
                print(f"Warning: truncating line {line_number} to {Charlimit-1} characters", file=sys.stderr, flush=True)
                line = line[:Charlimit-1] + '\n'
            buffered_length += len(line)
            if buffered_length >= Charlimit:
                merge_translation(to_translate, not_translate, output_lines)
                to_translate = []
                not_translate = []
                buffered_length = len(line)
            to_translate.append(line)
            not_translate.append(None)
        merge_translation(to_translate, not_translate, output_lines)
        return output_lines

    def translate_text_file(self, in_filename, out_filename):
        """ Read input file and write translation to output file. """
        output_lines = []
        with open(in_filename, encoding=self.encoding) as input:
            lines = input.readlines()
        try:
            self.translate_lines(lines, output_lines)
        finally:
            if Keep_incomplete_files:
                # output at least as far as we got
                with open(out_filename, 'w', encoding=self.encoding) as output:
                    output.write(''.join(output_lines))
                return
        with open(out_filename, 'w', encoding=self.encoding) as output:
            output.write(''.join(output_lines))


def regex_filter(line, regex_data):
    """ Return True if line should not be translated """
    sign, regex = regex_data
    match = bool(regex.search(line.strip('\n')))
    return match ^ sign


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Google-translate any plain text file.",
        epilog="If you need a more clever filter than regex then you'll need to write a filter "
            "function based on the regex example filter in this program."
    )
    parser.add_argument('--version', action='version', version='0.0.1')
    parser.add_argument('--filter=', default='', dest='filter', help="Prefix filter with + or -. Translate only lines that +do or -don't match regex. e.g. --filter='+(^//)|(^#)'")
    parser.add_argument('-s', '--source_language', default='nl', help="Source language (2-letter ISO639-2 codes); default=nl")
    parser.add_argument('-t', '--target_language', default='en', help="Target language (2-letter ISO639-2 codes); default=en")
    parser.add_argument('--encoding', default='utf-8', help="Character encoding used to interpret the input and output files; default=utf-8")
    parser.add_argument("infile", type=str, help="Text file to translate")
    parser.add_argument("outfile", type=str, help="Destination for translation")

    args = parser.parse_args()

    filter = regex_data = None
    if args.filter:
        if not args.filter.startswith('-') and not args.filter.startswith('+'):
            raise Exception("filter argument must being with + or -")
        sign = args.filter[0] == '+'
        regex = re.compile(args.filter[1:])
        regex_data = sign, regex
        filter = regex_filter

    translator = Translator(in_lang=args.source_language, out_lang=args.target_language, encoding=args.encoding, line_filter=filter, filter_data=regex_data)
    translator.translate_text_file(args.infile, args.outfile)

if __name__ == '__main__':
    main()
