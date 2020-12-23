#%%
import pandas as pd
import requests
import bs4
from tqdm import tqdm
import time
import os
#%%
df = pd.read_csv('speeches.csv')
#%%
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
headers = {
    'User-Agent' : user_agent
}
#%%
save_dir = 'speeches'
for i in tqdm(range(len(df))):
    content = requests.get(df.loc[i, 'link'], headers=headers).text
    soup = bs4.BeautifulSoup(content)
    with open(os.path.join(save_dir, f'article_{i}.txt'), 'w', encoding='utf-8') as f:
        f.write(soup.find('article').text)
# %%
