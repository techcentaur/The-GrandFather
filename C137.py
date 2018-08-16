import os
import json
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from wordcloud import WordCloud
import data_preprocessing_shit as dps

from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
import nltk
import random
from operator import itemgetter


with open('processed_files/rick.json') as jd:
    rick = json.load(jd)
with open('processed_files/morty.json') as jd:
    morty = json.load(jd)


def make_wordcloud(text):
    # rickmask = np.array(Image.open('rick.png'))
    wordcloud = WordCloud(max_words=2000, max_font_size=50).generate(text)

    plt.figure(figsize=(16, 12))
    plt.imshow(wordcloud)
    plt.axis("off")
    # plt.tight_layout(pad=5)
    plt.savefig('mortycloud.png', dpi=800)
    # plt.show()

    return True

def bigram_cloud(toks):
    finder = BigramCollocationFinder.from_words(toks)
    bigram_measures = BigramAssocMeasures()
    scored = finder.score_ngrams(bigram_measures.raw_freq)

    scoredList = sorted(scored, key=itemgetter(1), reverse=True)

    word_dict = {}
 
    listLen = len(scoredList)
 
    for i in range(listLen):
        word_dict['_'.join(scoredList[i][0])] = scoredList[i][1]
 
    WC_height = 500
    WC_width = 1000
    WC_max_words = 100
     
    wordCloud = WordCloud(max_words=WC_max_words, height=WC_height, width=WC_width)
     
    wordCloud.generate_from_frequencies(word_dict)
     
    plt.title('Most frequently occurring bigrams connected with an underscore_')
    plt.imshow(wordCloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


text = morty['morty']
make_wordcloud(text)
