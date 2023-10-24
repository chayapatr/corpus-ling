from pythainlp.tokenize import word_tokenize
from pythainlp.tag import pos_tag

original = "./scrape/chayapatr/apollo-guidance-computer.txt"
save = "./tagged.txt"
with open(original, encoding="utf-8") as f:
    tokenized = word_tokenize(f.read())
    tagged = pos_tag(tokenized)
    with open(save, "w", encoding="utf-8") as g:
        w = []
        for i in tagged:
            if i[0] not in ["\n", " "]:
                w.append(f"{i[0]}_{i[1]}")
            else:
                print("hit", i)
                w.append(i[0])
        g.write("|".join(w))