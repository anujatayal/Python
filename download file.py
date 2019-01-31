import pandas as pd
import requests
from bs4 import BeautifulSoup
url='http://codex.cs.yale.edu/avi/db-book/db4/slide-dir/ch1-2.pdf'
resp=requests.get(url,stream=True)
with open("python_logo.pdf",'wb') as f:
    for chunk in resp.iter_content(chunk_size=1024):
        if chunk:
            f.write(chunk)
