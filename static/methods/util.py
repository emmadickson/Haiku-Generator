import re
from nltk.corpus import cmudict
import Constants
import corpus
from random import randint
import pipeline
d = cmudict.dict()
personal_OOV = {}

used_word = []

def keyword_extraction(document):
    scores = {word: corpus.tfidf(word, document, corpus.corpus) for word in document.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_words


def stop_words(unstoppable_text):
    # 0. Start Logging
    print '\nSTARTING STOP_WORDS'

    unstoppable_text = unstoppable_text.split()

    # 2. Hardcoded English stop words, edit at will
    english_stop_words = Constants.ENGLISH_STOP_WORDS

    # 3. Remove stop words from list and rejoin the text as a string
    stopped_words = [word for word in unstoppable_text if word.lower() not in english_stop_words]

    print "\nFINISHING STOP WORDS"
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
                                  "mes$", "kes$", "nce$", "rles$"]

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


def haiku_line(line_length, syllable_buckets, tfidf_scores):
    line = []
    random_number = randint(1, line_length-2)
    initial_list = list(syllable_buckets[random_number])
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
            line.append(word)
            used_word.append(word)
            break


    # Number of syllables in first line
    first_line_count = line_length - random_number;
    while first_line_count != 0:
        random_number = randint(1, first_line_count)
        first_line_count = first_line_count - random_number
        initial_list = list(syllable_buckets[random_number])
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
                line.append(word)
                used_word.append(word)
                break
    return line
