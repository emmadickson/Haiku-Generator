""" Constants used throughout the application """

# Stop Words
ENGLISH_STOP_WORDS = ["MR"]

# Language Rules
grammar_rules = {"VB": ["NNP", "DT"],
                 "VBN": ["NNP", "IN", "NNS", "NN"],
                 "NNP": ["NNP", "VBZ", "JJ", "VB"],
                 "CD": ["NNS", "VBG", "VBD", "VBZ"],
                 "CC": ["RB", "VBD", "JJ"],
                 "RB": ["VBZ", "NNS"],
                 "VBZ": ["IN"],
                 "VBG": ["DT", "NN", "IN"],
                 "MD": ["VBD", "VBZ", "VBP"],
                 "JJ": ["CC", "NNS", "RB", "NN"],
                 "PRP": ["DT", "RB", "JJ"],
                 "VBD": ["JJ"],
                 "TO": ["DT"],
                 "DT": ["VBG", "NN", "JJ"],
                 "IN": ["NN", "DT"],
                 "NNS": ["VBP", "VBZ","VBG"],
                 "VBP": ["DT"],
                 "PRP$": ["JJ", "NNS"],
                 "NN": ["VBZ", "VBG", "VBD"],
                 "PDT":["DT"],
                 "FW": ["NNS", "NN", "DT"]
                 }
starting_pos = ["VB", "VBG", "NN", "DT", "NNS", "IN"]

ending_pos = ["VBZ", "NNS", "NN", "NNP", "VB"]