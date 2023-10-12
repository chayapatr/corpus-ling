import os

from gensim.models.ldamodel import LdaModel
from gensim.corpora import Dictionary

keywords = ["ที่มา", "ต่างๆ", "สำหรับ", "the", "อวกาศ", "ดาราศาสตร์", "วันที่", "เวลา", "of", 'ต่าง ๆ']

import pythainlp.corpus as tc
from pythainlp.tokenize import word_tokenize
from pythainlp.summarize.keybert import KeyBERT

import re

chunk = lambda l, n: [l[i:i + n] for i in range(0, len(l), n)]  

negation = tc.thai_negations()
thai_stop = tc.thai_stopwords()
thai_sy = tc.thai_syllables()

def condition(x):
    return (
            bool(re.search("[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZกขคฆงจฉชซฌญฎฏฐฑฒณดตถธทนบปผฝพฟภมยรลฤวศษสหฬอฮเแาะำไใโิีึืุู่้๊๋็ั์ๆฯ๐๑๒๓๔๕๖๗๘๙ฦฃฅๅ๎ํ๚]+", x))
            and not x in negation and not x in thai_stop and not x in thai_sy
            and not x in keywords
        )

text_data = set()
files = os.listdir("flatten")

kb = KeyBERT()

for file in files:
    with open(f"flatten/{file}", "r") as f:
        # text = [*(filter(condition, f.read().split("|")))]
        tokenized = [*(filter(condition, f.read().split("|")))]
        print(tokenized)
        chunked = chunk(tokenized, 200)
        print(f"read {file}")
        for x in chunked:
            joined = " ".join(x)
            text = kb.extract_keywords(joined)
            print(text)
            text_data.update(text)

text_data = [*text_data]

# Create a dictionary of the text data
dictionary = Dictionary(text_data)
# Create a bag of words representation of the text data
bow_corpus = [dictionary.doc2bow(doc) for doc in text_data]
# Train the LDA model
lda_model = LdaModel(bow_corpus, num_topics=15, id2word=dictionary, passes=15)

import pyLDAvis.gensim
vis = pyLDAvis.gensim.prepare(lda_model, bow_corpus, dictionary)
# Print the topics
for topic in lda_model.print_topics():
    print(topic)

pyLDAvis.display(vis)