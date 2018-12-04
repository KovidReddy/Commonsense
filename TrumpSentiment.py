from nltk.corpus import stopwords
import string
import pandas as pd
from collections import Counter
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras.layers import Dense
from keras.utils.vis_utils import plot_model
import matplotlib.pyplot as plt
from keras.layers import Dropout
import numpy as np
# fetch the data from the excel sheet and convert it into vocabulary

# get the excel data
def load_excel(filepath):
    reader = pd.read_excel(filepath,sheet_name=0)
    article_list = []
    for elem in reader['a']:
        article_list.append(elem)
    return article_list

# Turn each of the documents into a list of tokens
def tokenize_doc(doc):

    tokens = doc.split()
    table  = str.maketrans('', '', string.punctuation)
    tokens = [w.translate(table) for w in tokens]
    tokens = [word for word in tokens if word.isalpha()]
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if not w in stop_words]
    tokens = [word for word in tokens if len(word) > 1]
    return tokens

article_list = load_excel('C:\\Users\\pylak\\Documents\\Fall_2018\\DV\\Project\\Trump\\Article.xlsx')
article_list_n = load_excel('C:\\Users\\pylak\\Documents\\Fall_2018\\DV\\Project\\Trump\\Article2.xlsx')
tokens = []
token = []
article_token = []
article_test = []
article_token_n = []
article_test_n = []
for count,article in enumerate(article_list):
    token = tokenize_doc(article)
    article_token.append(token)
    if count > 150:
        article_test.append(token)
    for t in token:
        tokens.append(t)

for count,article in enumerate(article_list_n):
    token = tokenize_doc(article)
    article_token_n.append(token)
    if count > 150:
        article_test_n.append(token)
    for t in token:
        tokens.append(t)

# Define the vocabulary
vocab = Counter()

# Add all the words to the vocabulary
vocab.update(tokens)

# Remove words that only occur once from the vocabulary
vocab = [k for k,c in vocab.items() if c >= 2]

vocab = set(vocab)

# filter the documents based on the vocabulary
tok1 = []
final_article = []
for tok in article_token:
    tok1 = [word for word in tok if (word in vocab)]
    final_article.append(tok1)

final_article_test = []
for tok in article_test:
    tok1 = [word for word in tok if (word in vocab)]
    final_article_test.append(tok1)

final_article_n = []
for tok in article_token_n:
    tok1 = [word for word in tok if (word in vocab)]
    final_article_n.append(tok1)

final_article_test_n = []
for tok in article_test_n:
    tok1 = [word for word in tok if (word in vocab)]
    final_article_test_n.append(tok1)

# create tokenizer
tokenizer = Tokenizer()

# Combine the negative and positive
docs = article_token_n + article_token

# Create the vector models
tokenizer.fit_on_texts(docs)

# Encode the training data
Xtrain = tokenizer.texts_to_matrix(docs, mode='freq')
ytrain = np.array([0 for _ in range(len(article_token_n))] + [1 for _ in range(len(article_token))] )

# Load all the test data
docs = article_test_n + article_test

# Encode the test data
Xtest = tokenizer.texts_to_matrix(docs, mode='freq')
ytest = np.array([0 for _ in range(len(article_test_n))] + [1 for _ in range(len(article_test))] )

n_words = Xtest.shape[1]


# define network
model = Sequential()
model.add(Dense(50, input_shape=(n_words,), activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# compile network
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# fit network
model.fit(Xtrain, ytrain, epochs=100, verbose=2)

#evaluate
loss,acc = model.evaluate(Xtest, ytest, verbose=0)
print('Test Accuracy: %f' %(acc*100))

# history = model.fit(Xtrain, ytrain, epochs=100, verbose=2)
# # list all data in history
# print(history.history.keys())
# # summarize history for accuracy
# plt.plot(history.history['acc'])
# plt.title('model accuracy')
# plt.ylabel('accuracy')
# plt.xlabel('epoch')
# plt.legend(['train', 'test'], loc='upper left')
# plt.show()
# # summarize history for loss
# plt.plot(history.history['loss'])
# plt.title('model loss')
# plt.ylabel('loss')
# plt.xlabel('epoch')
# plt.legend(['train', 'test'], loc='upper left')
# plt.show()


# Test Articles
testart = load_excel('C:\\Users\\pylak\\Documents\\Fall_2018\\DV\\Project\\Trump\\TESTArticle.xlsx')
final_testart = []
testarty = []
for article in testart:
    token = tokenize_doc(article)
    testarty.append(token)

for tok in testarty:
    tok1 = [word for word in tok if (word in vocab)]
    final_testart.append(tok1)

for elem in final_testart:
    line = ' '.join(elem)
    encoded = tokenizer.texts_to_matrix([line], mode='freq')
    yhat = model.predict(encoded, verbose=0)
    print(yhat[0, 0])
    line = ''
    encoded = ''
