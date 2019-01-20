import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
import re #regular expressions
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

count_vectorizer=CountVectorizer()
transformer=TfidfTransformer()

file=open('training_file.txt','r')
#file1=open('output.txt','w')
data=[]
x_train=[]
y_data=[]
i=0
for line in file:
    if i==0:
        i=line
    else:
        x=line.strip().split('\t')
        x_train.append(x[0])
        y_data.append(x[1])
#print x_train
#print 'Hiiiiiiiiii'
#print y_train
y_data=np.asarray(y_data)
print type(y_data)
print y_data.shape
y=pd.factorize(y_data)
#print label
#print len(y)
#print y
y_train=y[0]
x_train=np.asarray(x_train)
df=pd.DataFrame({'id':y_train,'product':x_train,'type':y_data})
df.to_csv('output.csv')
df1=pd.DataFrame(y[1])
print df
#print type(y_train)
#print y_train.shape
print x_train.shape
#print type(x_train)
#print "string", y[1]
X_train,x_test,Y_train,y_test=train_test_split(x_train,y_train,test_size=0.3,random_state=1)

count_train=count_vectorizer.fit(X_train)
bag_of_words=count_vectorizer.transform(X_train)
#print bag_of_words.toarray()
#print("Every feature:\n{}".format(count_vectorizer.get_feature_names()))
print("Vocabulary size: {}".format(len(count_train.vocabulary_)))
#print("Vocabulary content:\n {}".format(count_train.vocabulary_))
count_train_tf=transformer.fit(bag_of_words)
bag_of_words_tf=transformer.transform(bag_of_words)
#print bag_of_words_tf.toarray()

#print x_train_counts.shape
clf=MultinomialNB().fit(bag_of_words_tf,Y_train)
#print y_test
print "Heyy"
#print Y_train
#print type(x_test)
predicted=clf.predict(count_vectorizer.transform(x_test))
df=pd.DataFrame({'predicted_id':predicted,'predicted':y[1][predicted], 'product':x_test,'type_id':y_test,'type':y[1][y_test]})
df.to_csv('output1.csv')
#print predicted
print metrics.accuracy_score(y_test,predicted)

