from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
import re
from nltk.stem.wordnet import WordNetLemmatizer
import enchant
import os
import time
import pwinput


def clrscr():
    clear = lambda: os.system("cls")
    clear()


def login():
    password = ""
    while password != "school":
        clrscr()
        print("  WELCOME\n===========\n\nUser : Administrator")
        password = pwinput.pwinput(prompt="Password : ")
        if password != "school":
            print("\nWrong Password !!\nTry Again")
        else:
            print("\nLogin Successful\nLoading Site...")
        time.sleep(3)
    clrscr()


def read_file(filename):
    model_answer = open(filename, "r")
    return model_answer.read()


def lemmatizer(words):
    l = [WordNetLemmatizer().lemmatize(w) for w in words]
    return l


def no_stopwords(words):
    s = []
    for w in words:
        if w not in stopwords.words("english"):
            s.append(w)
    return s


def misspelled(words):
    dictionary = enchant.Dict("en_IN")
    m = []
    for i in words:
        if not dictionary.check(i):
            m.append(i)
    return m


def syn_vector(obj):
    synonyms = []
    for syn in wordnet.synsets(obj):
        for i in syn.lemmas():
            synonyms.append(i.name())
    return synonyms


def unique(sequence):
    seen = set()
    return [z for z in sequence if not (z in seen or seen.add(z))]


def synonym_equaliser(text1, text2):
    for w in range(0, len(text2)):
        for d in unique(syn_vector(text2[w])):
            for y in text1:
                if d == y:
                    text2[w] = y
    return text2


def vectorize(set_of_words, doc_text):
    vector = []
    for i in set_of_words:
        vector.append(doc_text.count(i))
    return vector


def BoW(text1, text2):
    vocab = unique(text1 + text2)
    bow1 = vectorize(vocab, text1)
    bow2 = vectorize(vocab, text2)
    return [vocab, bow1, bow2]


def marking(vocab, bow1, bow2, num_misspelled, num_word, total_marks, text1):
    sum_large = 0
    sum_small = 0
    num_large1 = 0
    num_small1 = 0
    for i in text1:
        if len(i) > 5:
            num_large1 += 1
        else:
            num_small1 += 1
    ratio = (num_small1 + num_large1)/num_large1
    coef_large = ratio*total_marks/num_word
    coef_small = total_marks/num_word
    for i in text1:
        if len(i) > 5:
            sum_large += coef_large
        else:
            sum_small += coef_small
    total = sum_small + sum_large
    change = total_marks/total
    coef_large = change*coef_large
    coef_small = change*coef_small
    student_mark = 0
    for i in range(len(vocab)):
        if bow1[i] > 0:
            if len(vocab[i]) > 5:
                student_mark += bow2[i]*coef_large
            else:
                student_mark += bow2[i]*coef_small
    student_mark = student_mark - (num_misspelled/num_word)*3
    return student_mark


# Main

login()
answer_name = str(input("Enter Filename of Student Answer Sheet : "))

model_text = read_file("Model_Answer.txt")
answer_text = read_file(answer_name+".txt")

model_text_list = word_tokenize(re.sub(r"[^A-Za-z\d]", " ", model_text.lower()))
answer_text_list = word_tokenize(re.sub(r"[^A-Za-z\d]", " ", answer_text.lower()))

l_model = lemmatizer(model_text_list)
l_student = lemmatizer(answer_text_list)

l_s_model = no_stopwords(l_model)
l_s_student = no_stopwords(l_student)

sp_mistakes = misspelled(answer_text_list)

l_s_student1 = synonym_equaliser(l_s_model, l_s_student)
b = BoW(l_s_model, l_s_student1)

marks = marking(b[0], b[1], b[2], len(sp_mistakes), len(l_s_model), 50.0, l_s_model)
print("The Marks are : ", marks)
