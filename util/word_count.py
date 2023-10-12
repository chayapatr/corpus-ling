from pythainlp.tokenize import word_tokenize
import codecs
import os

def tokenize_string(filename):
    with open(f"scrape/{filename}", encoding="utf-8") as f:
        text = f.read()
        return len(word_tokenize(text, engine="newmm"))

authors = os.listdir('scrape')
overall_length = 0

for author in authors:
    articles = os.listdir(f'scrape/{author}')

    author_length = 0
    for article in articles:
        length = tokenize_string(f"{author}/{article}")
        author_length += length
    
    overall_length += author_length
    print(f"{author}: {author_length} words")

print(f"overall: {overall_length} words")