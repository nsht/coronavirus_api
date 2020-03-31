import requests
from app.secrets import *

def get_news(country_name="in"):
    url = f"http://newsapi.org/v2/top-headlines?q=coronavirus\
        &sortBy=popularity&country={country_name}&apiKey={NEWS_API_KEY}"
    data = requests.get(url)
    if data.status_code == 200:
        data = data.json()
        return data
