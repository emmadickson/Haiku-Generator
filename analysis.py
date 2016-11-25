import nltk
import re
from nltk.corpus import cmudict
import curses
from curses.ascii import isdigit


d = cmudict.dict()


def syllable_count(word):
    s = " "

    if word in d:
        lists = d[word]
        pronounciation = s.join(lists[0])
        print word + " and its pronounciation " + pronounciation
        print len(re.findall('\d+', pronounciation))

    print "OOV word encountered"
    subtract_syllables = ["cial", "tia", "cius", "cious", "uiet", "gious", "priest", "giu", "dge", "e$", "des$",
                          "mes$", "kes$", "nce$", "rles$"]
    add_syllables = ["ia", "riet", "dien", "ien", "iet", "iu", "iest", "io", "ii", "ily", "oala$", "iara$", "ying$",
                     "eate$", "eation$"]
    subtract_total = 0
    addition_total = 0

    for subtract in subtract_syllables:
        if re.search(subtract, word) != None:
            subtract_total += 1
    for add in add_syllables:
        if re.search(add, word) != None:
            addition_total += 1

    print "original word " + word

    word = re.compile("[^aeiouy]").split(word)
    for w in word:
        if w == '':
            word.remove(w)
    syllable_count = len(word) - subtract_total + addition_total
    print syllable_count

syllable_count("caterpillar")