import re, os
import glob, json

class Process:
    def __init__(self):
        self.dialogues = {'Rick':[], 'Morty':[]}

    def get_dialogues(self, file):
        with open(file, 'r') as f:
            lines = f.readlines()

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

    def get_data(self):
        files = glob.glob('./dataset/*/*.txt')

        for file in files:
            self.get_dialogues(file)

    @staticmethod
    def get_json(filename, filedata):
        with open(filename, 'w') as outfile:
            json.dump(filedata, outfile, sort_keys=True, indent=4)

        return os.path.abspath(os.path.dirname(filename))

if __name__=="__main__":
    p = Process()
    p.get_data()
    p.get_json('dilogue_data.json', p.dialogues)

    for name in ["rick", "morty"]:
        dial_ = []
        for key, valuelist in p.dialogues.items():
            if name in key.lower() and len(valuelist)>20:
                dial_.append(" ".join(valuelist))

        dial_ = " ".join(dial_)
        dial_ = dial_.replace('\n', '')
        p.get_json(name+'.json', {name: dial_})