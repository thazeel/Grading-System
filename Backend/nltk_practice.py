# Demonstrates different functions from the nltk library
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import re
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import enchant

text = "An appl is red in colour. It grows on treees. It is a fruit." # Try running program using various other sentences

print("Sent_Tokenize : ", sent_tokenize(text))
print("Word_Tokenize : ", word_tokenize(text))

split_text = text.split()

# Using re.sub function to remove punctuation marks so as to get words only
words = word_tokenize(re.sub(r"[^A-Za-z\d]", " ", text.lower()))
print("The words in the answer are : ", words)

print("Split Function : ", split_text)

words_without_stopwords = []
# Stopwords are words such as 'i', 'me', 'you', etc. which we avoid because we only need the major keywords in an answer
# to grade it.

for w in words:
    if w not in stopwords.words("english"):
        words_without_stopwords.append(w)

print("Words excluding Stopwords : ", words_without_stopwords)

# Stemming (gives base word, ie, removes '-ing', '-fully', etc.)
stemmed_words = [PorterStemmer().stem(w) for w in words_without_stopwords]
print("Stemmed Words : ", stemmed_words)

# Lemmatization (more accurate Stemming but takes time)
lemmatized_words = [WordNetLemmatizer().lemmatize(w) for w in words_without_stopwords]
print("Lemmatized Words : ", lemmatized_words)

# Part of Speech Tagging (Tags each word as a Noun, Verb, etc.)
tagged = nltk.pos_tag(lemmatized_words)
print("Tagged : ", tagged)

# Counting Number of Words (considering only the keywords in an answer)
number_of_words = len(words_without_stopwords)
print("Number of Keywords in the answer is : ", number_of_words)

# Finding words with Spelling Mistakes
dictionary = enchant.Dict("en_IN")
misspelled = []

for i in words:
    if not dictionary.check(i):
        misspelled.append(i)

number_misspelled = len(misspelled)
print("The misspelled words are : " + str(misspelled), "\nTotal number of misspelled words are : ", number_misspelled)
