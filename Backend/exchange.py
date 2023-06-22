from nltk .corpus import wordnet
import re
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords


def syn_vector(obj):
    synonyms = []
    for syn in wordnet.synsets(obj):
        for i in syn.lemmas():
            synonyms.append(i.name())
    return synonyms


def unique(sequence):
    seen = set()
    return [z for z in sequence if not (z in seen or seen.add(z))]


text1 = "That jump affect a lot"
text2 = "That leap made a lot of impact"
text1 = word_tokenize(re.sub(r"[^A-Za-z\d]", " ", text1.lower()))
text2 = word_tokenize(re.sub(r"[^A-Za-z\d]", " ", text2.lower()))

s_text1 = []
s_text2 = []

for word in text1:
    if word not in stopwords.words("english"):
        s_text1.append(word)
for word in text2:
    if word not in stopwords.words("english"):
        s_text2.append(word)

l_text1 = [WordNetLemmatizer().lemmatize(w) for w in s_text1]
l_text2 = [WordNetLemmatizer().lemmatize(w) for w in s_text2]
print(l_text1)
print(l_text2)

print("Text1 : ", l_text1)
print("Text2 : ", l_text2)

for w in range(len(l_text2)):
    for x in range(len(unique(syn_vector(l_text2[w])))):
        for y in range(len(l_text1)):
            if unique(syn_vector(l_text2[w]))[x] == l_text1[y]:
                l_text2[w] = l_text1[y]

print("Text2 : ", l_text2)
