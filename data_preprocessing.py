import re
import glob

class Process:
    def __init__(self):

    def form_dialogues(self):
        with open('dataset/season1.txt', 'r') as f:
            lines = f.readlines()

        dialogues = {'Rick':[], 'Morty':[]}

        for l in lines:
            lsplit = l.split(':', 1)
            
            # append only if a dialogue
            if len(lsplit) > 1:

                # remove the situation description
                lsplit[1] = re.sub("[\(\[].*?[\)\]]", "", lsplit[1])
                if lsplit[0] in dialogues:
                    dialogues[lsplit[0]].append(lsplit[1])
                else:
                    dialogues[lsplit[0]] = [lsplit[1]]

    def get_data(self):
        files = glob.glob('./dataset/*/*.txt')

        