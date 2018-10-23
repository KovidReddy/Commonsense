import warc
import html2text
import re
from bs4.element import Comment
from bs4 import BeautifulSoup
import nltk.data
import csv
import string
warc_count = ""
warc_path = ""
# Tokenizer
tokeniser = nltk.data.load('tokenizers/punkt/english.pickle')
final_list = []
count = 0
filename = "WarcOutput"
filepath = ""

ext = ".txt"

# Function to count the number of words
def count_words(words):
    nonPunct = re.compile('.*[A-Za-z0-9].*')
    count = 0
    # split the words and count the words that belong to the Non punctuation Category
    words_split = words.split()
    for word in words_split:
        if nonPunct.match(word):
            count = count + 1
    return count

# Change the range to suit your file sequences, by default it will be running for 0-20
for i in range(1,5):
    warc_count = str(i).zfill(2)
    warc_path = '0100wb-' + warc_count + ".warc.gz"
    # Open the WARC file
    f = warc.open(warc_path)
    print("Open file:", warc_count )
    filecount = 0
    for record in f:
        count = count + 1
        text = record.payload.read()
        soup = BeautifulSoup(text,'html.parser')
        table = soup.findAll('p')
        for x in table:
            text = re.sub('<.*>','',x.text, flags=re.DOTALL)
            text = re.sub('<!--.*-->', '', text, flags=re.DOTALL)
            text = text.replace('\n', '. ')
            text = text.replace('|','')
            match_obj = re.match(r'(.*)(lead to|leads to|led to|leading to|give rise to|gave rise to|given rise to|giving rise to|induce|inducing|induced|induces|cause|causes|causing|caused|caused by|bring on|brings on|brought on|bringing on|result from|resulting from|results from|resulted from|, because|because|because of|, thus|, therefore|, inasmuch as|due to|in consequence of|owing to|as a result of|and hence|as a consequence of|, hence|, consequently|and consequently|, for this reason alone ,)(.*)',text,re.M|re.I)
            if match_obj:
                sentences = nltk.sent_tokenize(text)
                sentences = [x for x in sentences if count_words(x) > 4]
                for y in sentences:
                    y = y.replace('\\', '')
                    final_list.append(y)
        if count > 5000:
            count = 0
            filecount = filecount + 1
            filepath = filename + warc_count + '-' + str(filecount) + ext
            with open(filepath, mode='w', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter="\n")
                writer.writerow(final_list)
            final_list = []
            print("done file:", filecount)

    # Test Console output
    print('done')


