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

    tridicts = util.pos_tag_tri(lower)
    pos_dict_tri = tridicts[0]
    word_dict_tri = tridicts[1]
    bidicts = util.pos_tag_bi(lower)
    pos_dict_bi = bidicts[0]
    word_dict_bi = bidicts[1]
    text = tb(lower)

    #corpus.corpus.append(text)

    tfidf_scores = util.keyword_extraction(text)
    line = []
    line1 = util.haiku_line(5, pos_dict_tri, pos_dict_bi, word_dict_tri, word_dict_bi, tfidf_scores, line, start=True, end=False)
    line2 = util.haiku_line(7, pos_dict_tri, pos_dict_bi, word_dict_tri, word_dict_bi, tfidf_scores, line1, start=False, end=False)
    test = line1+line2
    line3 = util.haiku_line(5, pos_dict_tri, pos_dict_bi, word_dict_tri, word_dict_bi, tfidf_scores, test, start=False, end=True)
    haiku = line1+line2 + line3
    print("--- %s seconds ---" % (time.time() - start_time))
    return "\n".join(haiku)
