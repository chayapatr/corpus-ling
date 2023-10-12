import os

authors = os.listdir("tokenized")

for author in authors:
    files = os.listdir(f"tokenized/{author}")
    for file in files:
        os.system(f"cp tokenized/{author}/{file} flatten/{author}_{file}")