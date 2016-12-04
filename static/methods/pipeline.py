import util
import corpus
from textblob import TextBlob as tb
import re
import time


def pipeline(text):
    start_time = time.time()
    # Eliminate uppercase
    lower = util.eliminate_upper(text)
    lower = lower.lower()
    lower = lower.encode('ascii', 'ignore')
    lower = lower.encode('utf-8')

    # Eliminate extraneous characters
    lower = re.sub('[!@#$,.;_()?]', '', lower)

    # Eliminate stop words
    stopped_text = util.stop_words(lower)

    # Test out Pos tagging
    dicts = util.pos_tag(lower)
    word_dict = dicts[1]
    pos_dict = dicts[0]
    # Join text and add it to the corpus
    edit_text = " ".join(stopped_text)
    test = tb(edit_text)
    corpus.corpus.append(test)

    # Get the tfidf score for the document
    tfidf_scores = util.keyword_extraction(test)
    # Put all the syllables into appropriate buckets.
    syll_buckets = util.syllable_bucket(edit_text)

    haiku = []
    line_one = util.haiku_line(5, syll_buckets, tfidf_scores, pos_dict, word_dict)
    line_one = " ".join(line_one)
    haiku.append(line_one)
    line_two = util.haiku_line(7, syll_buckets, tfidf_scores, pos_dict, word_dict)
    line_two = " ".join(line_two)
    haiku.append(line_two)
    line_three = util.haiku_line(5, syll_buckets, tfidf_scores, pos_dict, word_dict)
    line_three = " ".join(line_three)
    haiku.append(line_three)
    print("--- %s seconds ---" % (time.time() - start_time))
    return u'\n'.join(haiku).encode('utf-8')
