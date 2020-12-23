#%%
import pandas as pd
import numpy as np 
import sklearn
import re

from collections import Counter
import seaborn as sns

import matplotlib.pyplot as plt
from tqdm.std import TqdmMonitorWarning

from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer

from tqdm import tqdm
from numpy.core.fromnumeric import argmin
from scipy import stats
import os 
# %%
remove_hindi = lambda text: ''.join([char for char in text if ord(char) < 200])
fix_whitespaces = lambda  text : re.sub('[\s]+', ' ', text)
remove_punctuation = lambda text: re.sub('[^\w\s]', '', text)
remove_num = lambda text: re.sub('[0-9]+', '', text)
pre_process = lambda text : remove_num(remove_punctuation(fix_whitespaces(remove_hindi(text))))
#%%
data = {
    'text' : [],
    'economy_count' : [], 
    'precedent' : []
}

speech_dir = 'speeches'
for file_name in os.listdir(speech_dir):
    file_name = os.path.join(speech_dir, file_name)
    with open(file_name, 'r', encoding='utf-8') as f:
        text = f.read().lower().strip()
        text = pre_process(text)
        words = text.split()
    
    if 'economy' in words:
        one_grams = [words[i-1] for i, e in enumerate(words) if e == 'economy' and i > 0]
        economy_count = len(one_grams)
        
        data['text'].append(text)
        data['economy_count'].append(economy_count)
        data['precedent'].append(one_grams)

df = pd.DataFrame(data)
df
#%%
cnt = Counter()
prec = Counter()

for text in df['text'].values:
    for word in text.split():
        cnt[word] += 1

for pre in df['precedent'].values:
    for word in pre:
        prec[word] += 1

print(prec.most_common(50))
print('\n')
print(cnt.most_common(25))

print('economy :')
print(cnt['economy'])
#%%
d = dict(cnt.most_common(25))

plt.figure(figsize=(20,5))
plt.bar(*zip(*d.items())) 
plt.show()
#%%
p = dict(prec.most_common(15))

plt.figure(figsize=(15,4))
plt.bar(*zip(*p.items()))
plt.show()
#%%
d = dict(cnt)
sns.set_style('dark')
plt.figure(figsize=(15,15))
wc = WordCloud(width=2000,height=1500, max_words=90).generate_from_frequencies(d)
plt.imshow(wc)
plt.show()
#%%
tfidf = TfidfVectorizer(lowercase=True, analyzer='word', stop_words='english', ngram_range=(1,1))
tfidfv = tfidf.fit_transform(data['text'])
feature_names = tfidf.get_feature_names()
max_val = tfidfv.max(axis=0).toarray().ravel()
d = dict(zip(feature_names, max_val))
# %%
for key in list(d.keys())[:50]:
    print(key, d[key])
#%% 
