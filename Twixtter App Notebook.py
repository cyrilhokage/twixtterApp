
# coding: utf-8

# # Mining data on twitter with python.

# Based on this article: https://marcobonzanini.com/2015/03/09/mining-twitter-data-with-python-part-2/

# Requirements:
# - TWEEPY 3.7
# - nltk
# - re
# - json
# - operator
# - collections
# - string

# In[1]:


import tweepy
from tweepy import OAuthHandler


# In[2]:


from tweepy import Stream
from tweepy.streaming import StreamListener


# In[11]:


from nltk.tokenize import word_tokenize


# In[24]:


import re, json


# In[29]:


import operator 
from collections import Counter


# In[31]:


from nltk.corpus import stopwords
import string


# In[61]:


from nltk import bigrams


# # Part 1: Collecting data

# In[3]:


consumer_key = 'RRZFSHS1Nw8xH4eRyBaftyFfh'
consumer_secret = 'xdw3qoO1OmwZsb95CpDNpY4X7nYOwwgGeAPN2y6oiI9xP6Xkbx'
access_token = '720396530759385088-8bQxnzGDXXGHQB63eumuFYWnmL4nF6H'
access_token_secret = 'by2vprExn9FF4Sg2QJupvpZqhyiVYBr62FjB2VhkF0esv'


# In[4]:


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


# In[5]:


public_tweets = api.home_timeline()


# In[6]:


for tweet in public_tweets:
    print(tweet.text)


# In[7]:


status_list = []


# In[8]:


for status in tweepy.Cursor(api.home_timeline).items(10):
    # Process a single status
    status_list.append(status._json)


# Define a streaming listener

# In[10]:


class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('python.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True


# Launch a real time listener

# twitter_stream = Stream(auth, MyListener())
# twitter_stream.filter(track=['#python'])

# # Part 2: Text Pre-processing

# Create a tokenizer

# In[13]:


emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    


# In[14]:


tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)


# In[15]:


def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


# In[16]:


tweet = 'RT @marcobonzanini: just an example! :D http://example.com #NLP'
print(preprocess(tweet))


# In[22]:


tokens_list = []


# In[26]:


for status in status_list:
    tokens = preprocess(status['text'])
    tokens_list.append(tokens)


# In[28]:


tokens_list[0]


# # Part 3: Term Frequencies

# Importing stop-words

# In[48]:


punctuation = list(string.punctuation)
stop = stopwords.words('french') + punctuation + ['RT']


# In[60]:


count_all = Counter()
for status in status_list:
    
    # Create a list with all the terms
    terms_stop = [term for term in preprocess(status['text']) if term not in stop and not term.startswith(('#', '@'))]
    
    terms_hash = [term for term in preprocess(status['text']) if term.startswith('#')]
    
    # Update the counter
    count_all.update(terms_stop)
    
    # Print the first 5 most frequent words
    print(count_all.most_common(5))


# In[62]:


terms_bigram = bigrams(terms_stop)


# In[66]:


print(list(terms_bigram))

