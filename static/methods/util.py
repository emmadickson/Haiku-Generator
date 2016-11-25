import re
from nltk.corpus import cmudict
import Constants

d = cmudict.dict()
personal_OOV = {}


def stop_words(unstoppable_text):
    # 0. Start Logging
    print '\n STARTING STOP_WORDS: Input Type = ', type(unstoppable_text),  # ' Input Value = ', unstoppable_text

    unstoppable_text = unstoppable_text.split()

    # 2. Hardcoded English stop words, edit at will
    english_stop_words = Constants.ENGLISH_STOP_WORDS

    # 3. Remove stop words from list and rejoin the text as a string
    stopped_words = [word for word in unstoppable_text if word.lower() not in english_stop_words]

    print "\n FINISHING STOP WORDS"
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



syllable_count("caterpillar")
