import wikipedia
from wordcloud import WordCloud,STOPWORDS
import os
import requests
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

currdir=os.path.dirname(__file__)
def get_wiki(query):
    title = wikipedia.search(query)[0]
    page=wikipedia.page(title)
    return page.content

def transform_format(val):
    if val == 1:
        return 255
    else:
        return val

def create_wordcloud(text):
    #mask=np.array(Image.open(os.path.join(currdir,'wine.png')))
    #mask = np.array(Image.open(requests.get('http://www.clker.com/cliparts/O/i/x/Y/q/P/yellow-house-hi.png', stream=True).raw))
    mask=np.array(Image.open('twitter.png'))
    print(mask)
    transformed_wine_mask = np.ndarray((mask.shape[0],mask.shape[1]), np.int32)
    for i in range(len(mask)):
        transformed_wine_mask[i] = list(map(transform_format, mask[i]))

    print(transformed_wine_mask)
    stopwords=set(STOPWORDS)
    wc=WordCloud(background_color="white",max_words=1000, mask=transformed_wine_mask,stopwords=stopwords,contour_width=3, contour_color='firebrick')
    word_cloud=wc.generate(text)
    plt.figure(figsize=(10,8),facecolor = 'white', edgecolor='blue')
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()
    #wc.to_file(os.path.join(currdir,'word.png'))

create_wordcloud(get_wiki("python programming language"))
