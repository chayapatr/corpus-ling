from pythainlp.tokenize import word_tokenize
from pythainlp.tag import pos_tag

x = "./scrape/chayapatr/apollo-guidance-computer.txt"
with open(x, encoding="utf-8") as f:
    tokenized = word_tokenize(f.read())
    tagged = pos_tag(tokenized)
    print(tagged)