import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import re


def vectorize(set_of_words, doc_text):
    vector = []
    for i in set_of_words:
        vector.append(doc_text.count(i))
    return vector


def unique(sequence):
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]


model_answer = open(r"Model_Answer1.txt", "r")
text1 = model_answer.read()

student_answer = open(r"Student_Answer.txt", "r")
text2 = student_answer.read()

text1 = word_tokenize(re.sub(r"[^A-Za-z\d]", " ", text1.lower()))
text2 = word_tokenize(re.sub(r"[^A-Za-z\d]", " ", text2.lower()))

s_text1 = []
s_text2 = []

for w in text1:
    if w not in stopwords.words("english"):
        s_text1.append(w)
for w in text2:
    if w not in stopwords.words("english"):
        s_text2.append(w)

l_text1 = [WordNetLemmatizer().lemmatize(w) for w in s_text1]
l_text2 = [WordNetLemmatizer().lemmatize(w) for w in s_text2]
filtered_vocab = unique(l_text1+l_text2)

bow1 = vectorize(filtered_vocab, l_text1)
bow2 = vectorize(filtered_vocab, l_text2)
df_bow = pd.DataFrame([bow1, bow2], columns=filtered_vocab)
print(df_bow)
df_bow.to_excel(r"File Location", sheet_name="Sheet", index=False)
