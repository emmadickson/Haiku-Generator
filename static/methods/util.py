from __future__ import print_function
import re
import nltk
from operator import itemgetter
from nltk.tokenize import word_tokenize
from nltk.corpus import cmudict
import Constants
import corpus
from nltk.corpus import wordnet as wn
from random import randint
d = cmudict.dict()
personal_OOV = {}
lines = []
used_word = []


def eliminate_upper(text):
    split_text = text.split()
    not_upper = []
    for text in split_text:
        if text.isupper() is False:
            not_upper.append(text)

    return " ".join(not_upper)


def keyword_extraction(document):
    scores = {word: corpus.tfidf(word, document, corpus.corpus) for word in document.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_words


def syllable_count(word):
    s = " "
    word = word.lower()
    word = re.sub('[!-"@#,"?$]', '', word)

    if word.isdigit() is True:
        return 0

    if word in d:
        lists = d[word]
        pronunciation = s.join(lists[0])
        return len(re.findall('\d+', pronunciation))

    else:
        if word in personal_OOV:
            return personal_OOV[word]

        else:

            # print "OOV word encountered"
            # The reference from which we determine if we subtract or add syllables
            subtract_syllables = ["cial", "tia", "cius", "cious", "uiet", "gious", "priest", "giu", "dge", "e$", "des$",
                                  "mes$", "kes$", "nce$", "rles$", "ee"]

            add_syllables = ["ia", "mc", "riet", "dien", "ien", "iet", "iu", "iest", "io", "ii", "ily", "oala$", "iara$", "ying$",
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

            #print "original word " + word

            # Count the number of vowels in the word, this will be our original syllable count
            split_word = re.compile("[^aeiouy]").split(word)
            split_word = filter(None, split_word)

            # Calculate the final syllable count
            syllable_total = len(split_word) - subtract_total + addition_total
            #print syllable_total
            # Add total to OOV dict
            personal_OOV[word] = syllable_total

            # Return total syllable count
            return syllable_total


def syllable_bucket(edit_text):
    # Syllable bucket structure, a dictionary with the keys being syllable numbers and the value lists
    syllable_buckets = {}
    edit_text = edit_text.replace("-", " ")
    edit_text = edit_text.split(" ")

    # add things to syllable buckets
    for text in edit_text:
        if len(text) > 0:
            test = text
            if text[len(text) - 1].isalpha() is False:
                text = text[:-1]

            if test[0].isalpha() is False:
                text = text[:0] + text[(0 + 1):]

            syllable_c = syllable_count(text)

            if syllable_c != 0 and text.isupper() is False:
                if syllable_c in syllable_buckets.keys():
                    syllable_buckets[syllable_c].append(text)

                else:
                    syllable_buckets[syllable_c] = []
                    value_list = syllable_buckets[syllable_c]

                    if text not in value_list:
                        syllable_buckets[syllable_c].append(text)

    return syllable_buckets


def haiku_line(syllables, pos_dict, biposdict, word_dict, biword_dict, tfidf_scores, haiku, start, end):
    syllables_left = syllables
    # The list that will eventually become a list
    line = []

    corpus = []
    # Go through all the pos, if its one of the valid starting pos take the appropriate syllable
    # count list and add it to the corpus

    if start is True:
        for key in pos_dict.keys():
            real_keys = key.split()
            if real_keys[0] in Constants.starting_pos and pos_dict[key]:
                for k in pos_dict[key]:
                    if k == syllables_left and k != 0:
                        corpus = corpus + (list(pos_dict[key][k]))

        for key in biposdict.keys():
            bikeys = key.split()
            if bikeys[0] in Constants.starting_pos and biposdict[key]:
                for k in biposdict[key]:
                    if k == syllables_left and k != 0:
                        corpus = corpus + (list(biposdict[key][k]))

    else:
        lastkey = haiku[len(haiku) - 1].split()
        if len(lastkey) == 3:
            pos_list = (word_dict[haiku[len(haiku) - 1]]).split()
            pos_key = pos_list[2]
        else:
            pos_list = (biword_dict[haiku[len(haiku) - 1]]).split()
            pos_key = pos_list[1]
        for key in pos_dict.keys():
            real_keys = key.split()
            if end is not True:
                if real_keys[0] in Constants.grammar_rules[pos_key] and pos_dict[key]:
                    for k in pos_dict[key]:
                        if k == syllables_left and k != 0:
                            corpus = corpus + (list(pos_dict[key][k]))
            if end is True:
                if real_keys[0] in Constants.grammar_rules[pos_key] and pos_dict[key] and real_keys[2] in Constants.ending_pos:
                    for k in pos_dict[key]:
                        if k == syllables_left and k != 0:
                            corpus = corpus + (list(pos_dict[key][k]))

        for key in biposdict.keys():
            bikeys = key.split()
            if end is not True:
                if bikeys[0] in Constants.grammar_rules[pos_key] and biposdict[key]:
                    for k in biposdict[key]:
                        if k == syllables_left and k != 0:
                            corpus = corpus + (list(biposdict[key][k]))
            if end is True:
                if bikeys[0] in Constants.grammar_rules[pos_key] and biposdict[key] and bikeys[1] in Constants.ending_pos:
                    for k in biposdict[key]:
                        if k == syllables_left and k != 0:
                            corpus = corpus + (list(biposdict[key][k]))

    # Eliminate duplicates we just found some pos tags n there but w/e
    initial_set = set(corpus)
    initial_list = list(initial_set)
    tuple_list = []
    for init in initial_list:
        words = (init.split())

        if len(words) == 3:
            trigram = words[0] + " " + words[1] + " " + words[2]
            value1 = [item for item in tfidf_scores if item[0] == words[0]]
            value2 = [item for item in tfidf_scores if item[0] == words[1]]
            value3 = [item for item in tfidf_scores if item[0] == words[2]]
            if len(value1) !=0 and len(value2) !=0 and len(value3) != 0:
                total = (value1[0][1]) + (value2[0][1]) + (value3[0][1])
                tuple = (trigram, total)
                tuple_list.append(tuple)

        if len(words) == 2:
            bigram = words[0] + " " + words[1]
            value1 = [item for item in tfidf_scores if item[0] == words[0]]
            value2 = [item for item in tfidf_scores if item[0] == words[1]]
            if len(value1) !=0 and len(value2) !=0:
                total = (value1[0][1]) + (value2[0][1])
                tuple = (bigram, total)
                tuple_list.append(tuple)

    sorted_tuple_list = sorted(tuple_list, key=lambda x: x[1], reverse=True)
    for i in range(0, len(sorted_tuple_list)):
        if sorted_tuple_list[i][0] not in haiku and sorted_tuple_list[i][0] != 'group panoply slate':
            line.append(sorted_tuple_list[i][0])
            break
    return line


def pos_tag_tri(text):
    pos_dict = {}
    word_dict = {}

    tokens = word_tokenize(text)
    pos_list = nltk.pos_tag(tokens)

    tokens = pos_list
    shingles = [tokens[i:i + 3] for i in range(len(tokens) - 3 + 1)]
    for shingle in shingles:
        for i in range(0, len(shingle)-2, 3):
            # word = (shingle[i][0])
            # pos = (shingle[i][1])
            pos_combo = shingle[i][1] + " " + shingle[i+1][1] + " " + shingle[i+2][1]

            bigram = shingle[i][0] + " " + shingle[i + 1][0] + " " + shingle[i+2][0]
            if pos_combo in pos_dict.keys():
                count = syllable_count(bigram)
                if count in pos_dict[pos_combo].keys() and count != 0:
                    pos = pos_combo
                    pos_dict[pos][count].add(bigram)
                else:
                    syllable_count_list = set()
                    syllable_count_list.add(pos_combo)
                    pos_dict[pos_combo][count] = syllable_count_list

            else:
                syllable_dict = {}
                count = syllable_count(bigram)
                syllable_count_list = set()
                syllable_count_list.add(bigram)
                syllable_dict[count] = syllable_count_list
                pos_dict[pos_combo] = syllable_dict

            if bigram not in word_dict.keys():
                word_dict[bigram] = pos_combo
    return pos_dict, word_dict


def pos_tag_bi(text):
    pos_dict = {}
    word_dict = {}

    tokens = word_tokenize(text)
    pos_list = nltk.pos_tag(tokens)

    tokens = pos_list
    shingles = [tokens[i:i + 2] for i in range(len(tokens) - 2 + 1)]
    for shingle in shingles:
        for i in range(0, len(shingle)-1, 2):
            # word = (shingle[i][0])
            # pos = (shingle[i][1])
            pos_combo = shingle[i][1] + " " + shingle[i+1][1]
            bigram = shingle[i][0] + " " + shingle[i + 1][0]
            if pos_combo in pos_dict.keys():
                count = syllable_count(bigram)
                if count in pos_dict[pos_combo].keys() and count != 0:
                    pos = pos_combo
                    pos_dict[pos][count].add(bigram)
                else:
                    syllable_count_list = set()
                    syllable_count_list.add(pos_combo)
                    pos_dict[pos_combo][count] = syllable_count_list

            else:
                syllable_dict = {}
                count = syllable_count(bigram)
                syllable_count_list = set()
                syllable_count_list.add(bigram)
                syllable_dict[count] = syllable_count_list
                pos_dict[pos_combo] = syllable_dict

            if bigram not in word_dict.keys():
                word_dict[bigram] = pos_combo
    return pos_dict, word_dict