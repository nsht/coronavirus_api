from fastapi import FastAPI
from worldometer_scraper import get_data
from newsapi import get_news
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/stats")
def read_root():
    return get_data()


@app.get("/country/{country_name}")
def get_items(country_name):
    return get_data()["country_data"].get(
        country_name, {"status": False, "message": "Invalid Country name entered"}
    )


@app.get("/news/{country_name}")
def get_items(country_name):
    return get_news(country_name=country_name)


@app.get("/twitter_sentiment")
def get_twitter_sentiment(location=None, search_term=None):
    print(search_term)
    return main(location, search_term)
