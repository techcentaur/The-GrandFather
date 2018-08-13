import re, os
import glob, json, nltk
import click
import logging
import argparse

from string import punctuation
from nltk.corpus import stopwords


logger = logging.getLogger()


class TextClean(object):
    """For cleaning our d-d-dialogues Morty! We don't want shitty words polluting our shitty analysis"""

    def __init__(self):
        pass

    def apostrophe_normalisation(self, raw):
        """So, this is for normalizing the apostrophe, Grandpa Rick! -- Ye-Yeah! Morty. Good Job."""
        
        for (i, j) in [(r"n\'t", " not"), (r"\'re", " are"), (r"\'s", " is"), (r"\'d", " would"),
                        (r"\'ll", " will"), (r"\'t", " not"), (r"\'ve", " have"), (r"\'m", " am"),
                        (r"\'Cause", "because")]:
            raw = re.sub(i, j, raw)

        return raw

    def stopwords_remove(self, raw):                 
        """We'll kill all the stopwords here Morty! We'll remove the shit out of them from our tex-xt"""

        tokens = nltk.word_tokenize(raw)
        sw = set(stopwords.words('english'))

        clean_tokens = [x for x in tokens if not x in sw]
        text = self.punctuation_remove(clean_tokens)

        return text

    def punctuation_remove(self, tokens):
        """And remove the p-p-punctuations here! BTW Morty, I encourage you to use these in general! Grammar is cool Morty!"""
    
        punc_list = list(punctuation)

        for i in tokens:
            if i in punc_list:
                tokens.remove(i)
        
        text = " ".join(tokens)
        return text

    def clean(self, text):
        """Oh! Geez Rick! You used every function here -- Yeah, Morty! It's a custom function! It's *burps* function"""

        raw = self.apostrophe_normalisation(text)
        raw = self.stopwords_remove(raw)

        return raw



class Process:
    """A class for processing our dialogues Rick! That's so school!"""
    
    def __init__(self, loglevel):
        """It also has an initialize function Grandpa Rick! This adventure is gonna rock."""

        logger = loglevel
        self.dialogues = {'Rick':[], 'Morty':[]}

    def get_dialogues(self, file):
        """Don't get your hopes high Morty! And get the dialogues from here."""
        
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
        """This fu-unction will read scripts from our all seasons Morty! And this isn't even beginning."""

        files = glob.glob('./dataset/*/*.txt')

        logger.info('[*] Read scripts and collect d-d-dialogues here *burps* Morty!')
        
        with click.progressbar(range(len(files))) as progressbar:
            for progress in progressbar:
                self.get_dialogues(files[progress])

        print("[MORTY]: Processing is finished Rick! It's looking cool -- Should we g-go now?")
        print("[RICK]: No, Morty! The a-a-adventure begins here Morty! *burps* Let's go Morty! Let's go all out, and d-d-do our analysis Morty!\n")
        logger.debug('[*] WTF Morty! Is it finished y-y-yet?')

    
    @staticmethod
    def get_json(filename, filedata):
        """We'll save our dialogues in need from here! Remember this function Morty! It's called `get_json()`."""

        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:
                logger.debug('[!] Damn! Make a folder named `processed_files` by yourself; if not -- you l-l-lazy Jerry!')

        with open(filename, 'w') as outfile:
            json.dump(filedata, outfile, sort_keys=True, indent=4)

        return os.path.abspath(os.path.dirname(filename))

    def get_rick_and_morty(self):
        """Uhh!! A function with our name; which cleans our conversation. Man! This is amazing Rick, I love our adventures"""

        logger.info('[*] Create some JSON files for re-re-reading here M-Morty! We got no time!')
        
        for name in ["rick", "morty"]:
            dial_ = []
            
            for key, valuelist in self.dialogues.items():
                if name in key.lower() and len(valuelist)>20:
                    dial_.append(" ".join(valuelist))

            dial_ = " ".join(dial_)
            dial_ = dial_.replace('\n', '')

            clean_dial = TextClean().clean(dial_)

            self.get_json('./processed_files/' + name+'.json', {name: clean_dial})

        logger.info('[*]')
        logger.info('[*] Good *burps* job Morty!')



if __name__=="__main__":
    parser = argparse.ArgumentParser(description='The Grandfather: W-w-we\'ll process data here...Morty!')
    parser.add_argument('-l', '--loglevel', help='Set logging level M-Morty--But only in need.', type=str, choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL'])
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel)

    p = Process(args.loglevel)
    p.get_data()
    p.get_json('./processed_files/dilogue_data.json', p.dialogues)
    p.get_rick_and_morty()

