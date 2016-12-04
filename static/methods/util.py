from __future__ import print_function
import re
import nltk
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


def stop_words(unstoppable_text):
    unstoppable_text = unstoppable_text.split()

    # 2. Hardcoded English stop words, edit at will
    english_stop_words = Constants.ENGLISH_STOP_WORDS

    # 3. Remove stop words from list and rejoin the text as a string
    stopped_words = [word for word in unstoppable_text if word.lower() not in english_stop_words]

    return stopped_words


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


def haiku_line(line_length, syllable_buckets, tfidf_scores, pos_dict, word_dict):
    # The list that will eventually become a list

    line = []
    # The random syllable number
    random_number = randint(1, line_length - 2)

    corpus = []
    # Go through all the pos, if its one of the valid starting pos take the appropriate syllable
    # count list and add it to the corpus

    for key in pos_dict.keys():
        if key in Constants.starting_pos  and random_number in pos_dict[key]:
            corpus = corpus +(list(pos_dict[key][random_number]))

    # Eliminate duplicates we just found
    initial_set = set(corpus)
    initial_list = list(initial_set)

    # Calculate tfidf scores and add them to the tuple list
    tuple_list = []
    for init in initial_list:
        test = [item for item in tfidf_scores if item[0] == init]
        if len(test) > 0:
            tuple_list.append(test[0])
    # Sort the tuple list
    sorted_tuple_list = sorted(tuple_list, key=lambda x: x[1])

    # So at the first appropriate non used word we add it to the list and break
    for word, number in sorted_tuple_list:
        if word not in line and isinstance(word, basestring) and word not in used_word:
            #new_word = word[0].upper() + word[1:]
            line.append(word)
            lines.append(word)
            used_word.append(word)
            break

    # Number of syllables left in first line
    syllables_left = line_length - random_number


    # While we still need to add syllables to the line
    while syllables_left != 0:
        random_number = randint(1, syllables_left)
        last_word = lines[len(lines) - 1]
        print("last word " + last_word)
        last_pos = word_dict[last_word]
        corpus = []

        for key in pos_dict.keys():
            if key in Constants.grammar_rules[last_pos]:
                for k in pos_dict[key]:
                    if int(k) <= syllables_left:
                        corpus = corpus + (list(pos_dict[key][k]))

        if len(corpus) == 0:
            print ("HELP")
            for tfidf, word in tfidf_scores:
                if syllable_count(tfidf) <= syllables_left and len(tfidf) > 0:
                    tfidf = (str(tfidf))
                    corpus = corpus + ([tfidf])

            initial_set = set(corpus)
            initial_list = list(initial_set)
            tuple_list = []

            for init in initial_list:
                test = [item for item in tfidf_scores if item[0] == init]
                if len(test) > 0:
                    tuple_list.append(test[0])

            tuple_list = set(tuple_list)
            tuple_list = list(tuple_list)
            sorted_tuple_list = sorted(tuple_list, key=lambda x: x[1])

            for word, number in sorted_tuple_list:
                if word not in line and isinstance(word, basestring) and word not in used_word:
                    if len(line) > 0:
                        line.append(word)
                        lines.append(word)
                        used_word.append(word)
                        syllables_left = syllables_left - syllable_count(word)
                        break

            for i in line:
                print(i + " " + word_dict[i])
        else:

            initial_set = set(corpus)
            initial_list = list(initial_set)
            tuple_list = []

            for init in initial_list:
                test = [item for item in tfidf_scores if item[0] == init]
                if len(test) > 0:
                    tuple_list.append(test[0])

            tuple_list = set(tuple_list)
            tuple_list = list(tuple_list)
            sorted_tuple_list = sorted(tuple_list, key=lambda x: x[1])

            for word, number in sorted_tuple_list:
                if word not in line and isinstance(word, basestring) and word not in used_word:
                    if len(line) > 0:
                        line.append(word)
                        lines.append(word)
                        used_word.append(word)
                        syllables_left = syllables_left - syllable_count(word)
                        break
            for i in line:
                print(i + " " + word_dict[i])

    return line


def pos_tag(text):
    pos_dict = {}
    word_pos_dict = {}
    tokens = word_tokenize(text)
    pos_list = nltk.pos_tag(tokens)
    for pos, tag in pos_list:
        if tag in pos_dict.keys():
            count = syllable_count(pos)
            if count in pos_dict[tag].keys():
                pos_dict[tag][count].add(pos)
            else:
                count = syllable_count(pos)
                syllable_count_list = set()
                syllable_count_list.add(pos)
                pos_dict[tag][count] = syllable_count_list
        else:
            syllable_dict = {}
            count = syllable_count(pos)
            syllable_count_list = set()
            syllable_count_list.add(pos)
            syllable_dict[count] = syllable_count_list
            pos_dict[tag] = syllable_dict
        if pos not in word_pos_dict.keys():
            word_pos_dict[pos] = tag

    return pos_dict, word_pos_dict
