import util
import corpus
from textblob import TextBlob as tb



# Remember to make a haiku the syllable count is
# 5
# 7
# 5
# Chose first word radomly from a list of keywords ad then build off of those.


def pipeline(text):
    # Eliminate stop words
    stopped_text = util.stop_words(text)

    # Join text and add it to the corpus
    edit_text = " ".join(stopped_text)
    test = tb(edit_text)
    corpus.corpus.append(test)

    # Get the tfidf score for the document
    tfidf_scores = util.keyword_extraction(test)

    # Put all the syllables into appropriate buckets.
    syll_buckets = util.syllable_bucket(edit_text)

    haiku = []
    line_one = util.haiku_line(5, syll_buckets, tfidf_scores)
    line_one = " ".join(line_one)
    haiku.append(line_one)
    line_two = util.haiku_line(7, syll_buckets, tfidf_scores)
    line_two = " ".join(line_two)
    haiku.append(line_two)
    line_three = util.haiku_line(5, syll_buckets, tfidf_scores)
    line_three = " ".join(line_three)
    haiku.append(line_three)

    return str("\n".join(haiku))


