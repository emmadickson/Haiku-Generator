from __future__ import division, unicode_literals
import math
from textblob import TextBlob as tb
from nltk.corpus import brown
from nltk.corpus import reuters


document1 = tb(" ".join(reuters.words(fileids=['training/1'])))
document2 = tb(" ".join(reuters.words(fileids=['training/10'])))
document3 = tb(" ".join(reuters.words(fileids=['training/100'])))
document4 = tb(" ".join(reuters.words(fileids=['training/10000'])))
document5 = tb(" ".join(reuters.words(fileids=['training/9920'])))
document6 = tb(" ".join(reuters.words(fileids=['training/9923'])))
document7 = tb(" ".join(reuters.words(fileids=['training/9925'])))
document8 = tb(" ".join(reuters.words(fileids=['training/8179'])))
document9 = tb(" ".join(reuters.words(fileids=['training/7516'])))
document10 = tb(" ".join(reuters.words(fileids=['training/7490'])))
document11 = tb(" ".join(reuters.words(fileids=['training/6535'])))
document12 = tb(" ".join(reuters.words(fileids=['training/5682'])))
document13 = tb(" ".join(reuters.words(fileids=['training/5118'])))
document14 = tb(" ".join(reuters.words(fileids=['training/4498'])))
document15 = tb(" ".join(reuters.words(fileids=['training/4490'])))
document16 = tb(" ".join(reuters.words(fileids=['training/4120'])))
document17 = tb(" ".join(reuters.words(fileids=['training/400'])))
document18 = tb(" ".join(reuters.words(fileids=['training/3610'])))
document19 = tb(" ".join(reuters.words(fileids=['training/3595'])))
document20 = tb(" ".join(reuters.words(fileids=['training/2167'])))
document21 = tb(" ".join(reuters.words(fileids=['training/2137'])))
document22 = tb(" ".join(reuters.words(fileids=['training/2126'])))
document23 = tb(" ".join(reuters.words(fileids=['training/227'])))
document24 = tb(" ".join(reuters.words(fileids=['training/2570'])))
document25 = tb(" ".join(reuters.words(fileids=['training/517'])))
document26 = tb(" ".join(reuters.words(fileids=['training/9926'])))
document27 = tb(" ".join(reuters.words(fileids=['training/9927'])))
document28 = tb(" ".join(reuters.words(fileids=['training/5222'])))
document29 = tb(" ".join(reuters.words(fileids=['training/4914'])))
document30 = tb(" ".join(reuters.words(fileids=['training/5050'])))
document31 = tb(" ".join(reuters.words(fileids=['training/2810'])))
document32 = tb(" ".join(reuters.words(fileids=['training/2971'])))
document33 = tb(" ".join(reuters.words(fileids=['training/2864'])))
document34 = tb(" ".join(reuters.words(fileids=['training/2839'])))
document35 = tb(" ".join(reuters.words(fileids=['training/2952'])))
document36 = tb(" ".join(reuters.words(fileids=['training/3190'])))
document37 = tb(" ".join(reuters.words(fileids=['training/3228'])))
document38 = tb(" ".join(reuters.words(fileids=['training/354'])))
document39 = tb(" ".join(reuters.words(fileids=['training/4028'])))
document40 = tb(" ".join(reuters.words(fileids=['training/4033'])))
document41 = tb(" ".join(reuters.words(fileids=['training/4291'])))
document42 = tb(" ".join(reuters.words(fileids=['training/4603'])))
document43 = tb(" ".join(reuters.words(fileids=['training/5205'])))
document44 = tb(" ".join(reuters.words(fileids=['training/5287'])))
document45 = tb(" ".join(reuters.words(fileids=['training/528'])))
document46 = tb(" ".join(reuters.words(fileids=['training/702'])))
document47 = tb(" ".join(reuters.words(fileids=['training/7064'])))
document48 = tb(" ".join(reuters.words(fileids=['training/7052'])))
document49 = tb(" ".join(reuters.words(fileids=['training/7077'])))
document50 = tb(" ".join(reuters.words(fileids=['training/708'])))
document51 = tb(" ".join(brown.words(fileids=['ca16'])))
document52 = tb(" ".join(brown.words(fileids=['cb02'])))
document53 = tb(" ".join(brown.words(fileids=['cc17'])))
document54 = tb(" ".join(brown.words(fileids=['ch15'])))
document55 = tb(" ".join(brown.words(fileids=['cg22'])))


def tf(word, blob):
    return blob.words.count(word) / len(blob.words)


def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)


def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))


def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)


corpus = [
          document11, document12, document13, document14, document15, document16, document17, document18, document19,
          document20, document21, document22, document23, document24, document25, document26, document27, document28,
          document29, document30, document31, document32, document33, document34, document35, document36, document37,
          document38, document39, document40, document41, document42, document43, document44, document45, document46,
          document47, document48, document49, document50, document51, document52, document53, document54, document55,]