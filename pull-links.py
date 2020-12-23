#%%
import requests
import pandas as pd
import bs4
from tqdm import tqdm
import time
#%%
page_url = lambda i : f'https://www.narendramodi.in/speech/searchspeeche?language=en&page={i}&keyword=&fromdate=&todate='
#%%
# %%
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
headers = {
    'User-Agent' : user_agent
}
# %%
#%%
data = {
    'title' : [],
    'link' : []
}

for i in tqdm(range(50)):
    url = page_url(i)
    reponse = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(reponse.text)
    for box in soup.find_all('div', 'speechesBox'):
        speech = box.find('div', 'speechesItemLink')
        title = speech.text
        # print(title)
        data['title'].append(speech.text)
        data['link'].append(speech.find('a')['href'])
    time.sleep(1)
# %%
df = pd.DataFrame(data)
df.to_csv('speeches.csv', index=False)
# %%

# %%
