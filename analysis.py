import nltk
import re
from nltk.corpus import cmudict
import curses
from curses.ascii import isdigit


d = cmudict.dict()
personal_OOV = {}

def syllable_count(word):
    s = " "

    if word in d:
        lists = d[word]
        pronunciation = s.join(lists[0])
        # print word + " and its pronunciation " + pronunciation
        # print len(re.findall('\d+', pronunciation))
        return len(re.findall('\d+', pronunciation))

    else:
        if word in personal_OOV:
            return personal_OOV[word]
        else:

            # print "OOV word encountered"
            # The reference from which we determine if we subtract or add syllables
            subtract_syllables = ["cial", "tia", "cius", "cious", "uiet", "gious", "priest", "giu", "dge", "e$", "des$",
                                  "mes$", "kes$", "nce$", "rles$"]

            add_syllables = ["ia", "riet", "dien", "ien", "iet", "iu", "iest", "io", "ii", "ily", "oala$", "iara$", "ying$",
                             "eate$", "eation$"]

            # original totals
            subtract_total = 0
            addition_total = 0

            # Check using regex if we need to add or subtract syllables after determining vowel count

            for subtract in subtract_syllables:
                if re.search(subtract, word) is not None:
                    subtract_total += 1

            for add in add_syllables:
                if re.search(add, word) is not None:
                    addition_total += 1

            # print "original word " + word

            # Count the number of vowels in the word, this will be our original syllable count
            word = re.compile("[^aeiouy]").split(word)
            for w in word:
                if w == '':
                    word.remove(w)

            # Calculate the final syllable count
            syllable_total = len(word) - subtract_total + addition_total

            # Add total to OOV dict
            personal_OOV[word] = syllable_total

            # Return total syllable count
            return syllable_total


syllable_count("caterpillar")
