from genericpath import isfile
import os
from nltk.corpus import wordnet as wn

from googletrans import Translator, constants
# from deep_translator import PonsTranslator
# from deep_translator.exceptions import TranslationNotFound
from pprint import pprint
import matplotlib.pyplot as plt
from csv import reader
from numpy.lib.arraypad import _set_reflect_both
from numpy.lib.function_base import append
from spellchecker import SpellChecker
import numpy as np
import pandas as pd
import io_my

spell = SpellChecker(language="de")
translator = Translator()
print(translator.translate("word"))

#translator = PonsTranslator(source="de", target="en")
# goal : categorize words into given categories
#  

# read csv file as a list of lists


file = "https://docs.google.com/spreadsheets/d/xyz"
key = "123456"
gids = [0,291367008]
#filename = "data/expenses"
filename = "data/Test_Ausgaben.csv"
items = []

if not os.path.isfile("." + os.sep  + filename):
    io_my.download(key,gid=gids,outputfile=filename)

with open(filename + ".xls", 'r', encoding="UTF-8") as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Pass reader object to list() to get a list of lists
    items = list(csv_reader)



#print(items)

def sset(word):
    set_ =  wn.synsets(word)
    if set_!=[]:
        return set_[0]
    else:
        return []


def preprocess(word):
    l = len(word)
    result = word
    if len(word) == 0:
        return result
    while(result[l-1] == " "):
        result = result[:-1]
        l  = l -1
    result = result.replace(" ","_")
    return result

def preprocess_german(word):
    result = word
    substitutions = [
        ('ä', 'ae'),
        ('ö', 'oe'),
        ('ü', 'ue'),
        ("ß", "ss")
        ]
    for search, replacement in substitutions:
        result = result.replace(search, replacement)
    return result

translation_payed = []
    
for item in items:
    # consider misspelled words
    word = spell.correction(item[0])
    #print(f'{item[0]} -> {word}')
    word = preprocess_german(word)

    #try:
    translated = translator.translate(word,src="de",dest="en")
    # except TranslationNotFound as e:
    #     translated = word
    #print(f'{translated.origin} -> {translated.text}')
    
    
    new_word = preprocess(translated.text) 
    
     # check if synset exists other wise modify input
    if(not sset(new_word)):
        new_word = translated.text.split(" ")[0]
        new_word = preprocess(new_word)

    #print(f'preprocessed \n{translated.text} -> {new_word}')
    translation_payed.append((new_word,item[1]))

print(translation_payed)

categories = ['food', 'furniture', 
            'styling', 'office']

examples = ["mirror","soap","toilet", "apple","pencil","lipgloss","carpet","decoration"]

costs = [0,0,0,0]

word = "curtain"
roots = []

distribution = [0,0,0,0]
total = 0
# level = 10

syns = wn.synsets(word)

syn = syns[0]

# hy = syn.hyponyms()
# print(hy)

# print("level " + str(0)  + ": " + str(syn))
# for i in range(10):
#     syns = syn.hyponyms()
#     if syns!=[]:
#         syn = syns[0]
#     print("level " + str(i) + ": " + str(syn))

def iter_hyponym(syn,level, roots):
    hyps = syn.hyponyms()
    if hyps != []:
        counter = 1
        for hyp in hyps:
            print("level " + str((level,counter)) + ": " + str(hyp))
            counter = counter + 1
            iter_hyponym(hyp,level + 1,roots)
    else:
        #add synsets without parents to cluster list 
        roots.append(syn)

## similarity

uncategorized = []

for (ex,amount) in translation_payed:
    print((ex,amount))
    try:
        print("checking example " + ex)
        if not sset(ex):
            uncategorized.append(ex)
            print("no synset exists; not comparable")
        else:
            sim_vec1 = []
            sim_vec2 = []  
            for cat in categories:
                print("entered cat")
                #val = sset(ex).path_similarity(sset(cat), simulate_root=False)
                val2 = sset(ex).wup_similarity(sset(cat), simulate_root=False)
                #sim_vec1.append(val)
                sim_vec2.append(val2)
            res = [0 if v is None else v for v in sim_vec2]
            print("similarity vector:" + "\n " + str(res))
            m = max(res)
            if (m == 0):
                print("could not classify")
                continue
            i = res.index(m)
            distribution[i] = distribution[i] + 1
            costs[i] = costs[i] + int(amount)
            print("class: "+ categories[i])
        total = total + int(amount)
    except Exception as e:
        print(e)

print(distribution)

print(costs)

print("uncategorized" + str(uncategorized))
n_uncat = len(uncategorized)
# distribution[len(distribution) - 1] = n_uncat

fig, (ax1,ax2) = plt.subplots(2)
fig.suptitle(f'Expenses statistics. Unclassified:  { len(uncategorized)} from {len(items)}')

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = categories
sizes = distribution
explode = (0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=False, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.



ticks = np.arange(len(categories))
ax2.bar(categories,costs)

ax2.set_ylabel('Money')
ax2.set_title('Category')
ax2.set_yticks(np.arange(0, 1000, 200))
ax2.title.set_text("Cost distribution; total amount: " + str(total))

plt.show()