import PyPDF2
import gensim
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from string import punctuation
from heapq import nlargest

# Open the PDF file
pdfFileObj = open('book.pdf', 'rb')

# Read the PDF content
pdfReader = PyPDF2.PdfReader(pdfFileObj)
text = ''
for pageNum in range(pdfReader.numPages):
    pageObj = pdfReader.getPage(pageNum)
    text += pageObj.extractText()

# Tokenize the text
sentences = sent_tokenize(text)
words = word_tokenize(text.lower())

# Remove stop words and punctuation
stop_words = set(stopwords.words('english') + list(punctuation))
filtered_words = [word for word in words if word not in stop_words]

# Build the word frequency dictionary
word_freq = {}
for word in filtered_words:
    if word not in word_freq:
        word_freq[word] = 1
    else:
        word_freq[word] += 1

# Compute the weighted frequency scores for each sentence
sent_scores = {}
for sentence in sentences:
    for word in word_tokenize(sentence.lower()):
        if word in word_freq:
            if len(sentence.split()) < 30:
                if sentence not in sent_scores:
                    sent_scores[sentence] = word_freq[word]
                else:
                    sent_scores[sentence] += word_freq[word]

# Select the top N sentences with the highest scores
summary_sentences = nlargest(10, sent_scores, key=sent_scores.get)
summary = ' '.join(summary_sentences)

# Print the summary
print(summary)
