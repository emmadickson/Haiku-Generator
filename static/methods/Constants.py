""" Constants used throughout the application """

# Stop Words
ENGLISH_STOP_WORDS = [ "MR"]

# Language Rules
grammer_rules = {"NP": ["DT", "NG", "NN", "CC", "RB", "CD", "JJ", "PRP" "NNS"],
                 "NG": ["JJ", "NG", "NN"],
                 "PP": ["IN", "NP"],
                 "VP": ["MD", "VP", "VBD", "VBN", "SBAR", "VB", "PP", "VBP"],
                 "SBAR": ["IN"],
                 "ADJP": ["JJ", "PP"],
                 "NN": [],
                 "IN":[],
                 "VBP":[],
                 "VB":[],
                 "DT":[],
                 "CC":[],
                 "RB":["IN", "DT", "NN"],
                 "CD":[],
                 "JJ":["NNS", "NN"],
                 "PRP":[],
                 "NNS":["JJ", "DT", "IN", "ADJP", "VB", "VBG"],
                 "VBG":[],
                 "VBN":[],
                 "VBD":[],
                 "VBZ":[]
                 }