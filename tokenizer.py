from pythainlp.tokenize import word_tokenize
import os

def tokenize_string(filename):
    with open(f"scrape/{filename}", encoding="utf-8") as f:
        print(f"tokenize {filename}")
        text = f.read()
        return "|".join(word_tokenize(text, engine="newmm"))        

def write_file(filename, text):
    with open(f"{filename}", "w") as f:
        f.write(text)

authors = os.listdir('scrape')

for author in authors:
    articles = os.listdir(f'scrape/{author}')
    os.mkdir(f"tokenized/{author}")
    for article in articles:
        text = tokenize_string(f"{author}/{article}")
        write_file(f"tokenized/{author}/{article}", text)