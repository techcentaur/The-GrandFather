import re, os
import glob, json, nltk
import click
import logging
import argparse

from string import punctuation
from nltk.corpus import stopwords
logger = logging.getLogger()

class Process:
    def __init__(self, loglevel):
        logger = loglevel
        self.dialogues = {'Rick':[], 'Morty':[]}

    def get_dialogues(self, file):
        with open(file, 'r') as f:
            lines = f.readlines()

        try:
            for l in lines:
                lsplit = l.split(':', 1)
                # append only if a dialogue
                if len(lsplit) > 1:
                    # remove the situation description
                    lsplit[1] = re.sub("[\(\[].*?[\)\]]", "", lsplit[1])
                    if lsplit[0] in self.dialogues:
                        self.dialogues[lsplit[0]].append(lsplit[1])
                    else:
                        self.dialogues[lsplit[0]] = [lsplit[1]]
        except Exception as e:
            logger.debug('[!] Something is wrong in reading t-t-the file Morty! Check here, in-and-out, 20 minutes adventure!')

    def get_data(self):
        files = glob.glob('./dataset/*/*.txt')

        logger.info('[*] Read scripts and collect d-d-dialogues here *burps* Morty!')
        
        with click.progressbar(range(len(files))) as progressbar:
            for progress in progressbar:
                self.get_dialogues(files[progress])

        logger.info('[*] WTF Morty! Is it finished y-y-yet?')

    @staticmethod
    def get_json(filename, filedata):
        with open(filename, 'w') as outfile:
            json.dump(filedata, outfile, sort_keys=True, indent=4)

        return os.path.abspath(os.path.dirname(filename))

    def get_rick_and_morty(self):
        logger.info('[*] Create some JSON files for re-re-reading here M-Morty! We got no time!')
        
        for name in ["rick", "morty"]:
            dial_ = []
            
            for key, valuelist in self.dialogues.items():
                if name in key.lower() and len(valuelist)>20:
                    dial_.append(" ".join(valuelist))

            dial_ = " ".join(dial_)
            dial_ = dial_.replace('\n', '')

            clean_dial = TextClean().clean(dial_)

            self.get_json(name+'.json', {name: clean_dial})

        logger.info('[*]')
        logger.info('[*] Good *burps* job Morty!')



class TextClean(object):
    def __init__(self):
        pass

    def apostrophe_normalisation(self, raw):
            for (i, j) in [(r"n\'t", " not"), (r"\'re", " are"), (r"\'s", " is"), (r"\'d", " would"),
                            (r"\'ll", " will"), (r"\'t", " not"), (r"\'ve", " have"), (r"\'m", " am"),
                            (r"\'Cause", "because")]:
                raw = re.sub(i, j, raw)

            return raw

    def stopwords_remove(self, raw):                 
            tokens = nltk.word_tokenize(raw)
            sw = set(stopwords.words('english'))

            clean_tokens = [x for x in tokens if not x in sw]
            text = self.punctuation_remove(clean_tokens)

            return text

    def punctuation_remove(self, tokens):
            punc_list = list(punctuation)

            for i in tokens:
                if i in punc_list:
                    tokens.remove(i)
            
            text = " ".join(tokens)
            return text

    def clean(self, text):
        raw = self.apostrophe_normalisation(text)
        raw = self.stopwords_remove(raw)

        return raw


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='The Grandfather: W-w-we\'ll process data here...Morty!')
    parser.add_argument('-l', '--loglevel', help='Set logging level M-Morty--But only in need.', type=str, choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL'])
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel)

    p = Process(args.loglevel)
    p.get_data()
    p.get_json('dilogue_data.json', p.dialogues)
    p.get_rick_and_morty()

