from fastapi import FastAPI
from app.worldometer_scraper import get_data
from app.newsapi import get_news
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/stats",
    responses={
        200: {
            "description": "A list of dictionaries with all the stats",
            "content": {
                "application/json": {
                    "example": """
                    {
                        "country_data": {
                            "IN": {
                                {
                                    "country_name": "India",
                                    "total_cases": 1637,
                                    "new_cases": 240,
                                    "total_deaths": 45,
                                    "new_deaths": 10,
                                    "total_recovered": 148,
                                    "active_cases": 1444,
                                    "critical": "",
                                    "cases_per_million_pop": 1,
                                    "deaths_per_million_pop": 0.03,
                                    "1st_case_date": "Jan 29",
                                    "recovery_percentage": 9.04,
                                }
                            }
                        }
                    }
                    """
                }
            },
        }
    },
)
def get_stats():
    """ Returns statistics for every country and a worldwide total"""
    return get_data()


@app.get(
    "/country/{country_name}",
    responses={
        200: {
            "description": "The statistics for the given country",
            "content": {
                "application/json": {
                    "example": {
                        "country_name": "India",
                        "total_cases": 1637,
                        "new_cases": 240,
                        "total_deaths": 45,
                        "new_deaths": 10,
                        "total_recovered": 148,
                        "active_cases": 1444,
                        "critical": "",
                        "cases_per_million_pop": 1,
                        "deaths_per_million_pop": 0.03,
                        "1st_case_date": "Jan 29",
                        "recovery_percentage": 9.04,
                    }
                }
            },
        }
    },
)
def get_items(country_name: str):
    """ Returns statistics for the specified country. The country name should be in the
    3166-1 Alpha 2 format.
    """

    return get_data()["country_data"].get(
        country_name.upper(),
        {"status": False, "message": "Invalid Country name entered"},
    )


@app.get("/news/{country_name}", include_in_schema=False)
def get_items(country_name: str):
    return get_news(country_name=country_name)


@app.get("/twitter_sentiment", include_in_schema=False)
def get_twitter_sentiment(location: str = None, search_term: str = None):
    print(search_term)
    return main(location, search_term)
