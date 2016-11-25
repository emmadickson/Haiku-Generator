import util

# Syllable bucket structure, a dictionary with the keys being syllable numbers and the value lists
syllable_buckets = {}


def pipeline(text):
    stopped_text = util.stop_words(text)
    edit_text = " ".join(stopped_text)
    edit_text = edit_text.replace("-", " ")
    edit_text = edit_text.split(" ")

    for text in edit_text:
        test = text
        if text[len(text)-1].isalpha() is False:
            text = text[:-1]

        if test[0].isalpha() is False:
            text = text[:0] + text[(0 + 1):]

        syllable_count = util.syllable_count(text)

        if syllable_count != 0 and text.isupper() is False:
            if syllable_count in syllable_buckets.keys():
                syllable_buckets[syllable_count].add(text)

            else:
                syllable_buckets[syllable_count] = set()
                value_list = syllable_buckets[syllable_count]

                if text not in value_list:
                    syllable_buckets[syllable_count].add(text)

    return stopped_text

