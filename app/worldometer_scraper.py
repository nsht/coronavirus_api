import asyncio

import requests
from bs4 import BeautifulSoup

import pdb
from aiocache import Cache

from app.countries import *

data_pos = {
    0: "country_name",
    1: "total_cases",
    2: "new_cases",
    3: "total_deaths",
    4: "new_deaths",
    5: "total_recovered",
    6: "active_cases",
    7: "critical",
    8: "cases_per_million_pop",
    9: "deaths_per_million_pop",
    10: "total_tests",
    11: "tests_per_million",
}


def get_data():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    cache = Cache(Cache.REDIS, endpoint="redis", port=6379, namespace="corona_api",)
    cached_data = loop.run_until_complete(cache.get("all_stats"))
    if cached_data:
        return cached_data
    data = requests.get("https://www.worldometers.info/coronavirus/").text
    soup = BeautifulSoup(data, "html.parser")

    table = soup.find("table", id="main_table_countries_today")
    rows = table.findAll("tr")
    response = {}
    data_list = {}
    for row in rows:
        cols = [c for c in row.find_all("td")]
        country_data = {}
        for index, data in enumerate(cols):
            if data_pos.get(index):
                stat_number = data.text.strip().strip("+").replace(",", "")
                if stat_number.isdigit():
                    try:
                        stat_number = int(stat_number)
                    except ValueError as e:
                        print(f"Error converting to int for data {data}")
                else:
                    stat_number = process_float(stat_number)
                if stat_number == "":
                    stat_number = "NA"
                country_data[data_pos[index]] = stat_number

        if country_data.get("country_name"):
            if country_data["country_name"] == "Total:":
                country_data["country_name"] = "World"
            country_data["recovery_percentage"] = calculate_percentage(
                numerator=country_data["total_recovered"],
                denominator=country_data["total_cases"],
            )
            country_data["postive_test_percentage"] = calculate_percentage(
                numerator=country_data["total_cases"],
                denominator=country_data["total_tests"],
            )
            try:
                data_list[COUNTRY_LIST[country_data["country_name"]]] = country_data
            except:
                data_list[country_data["country_name"]] = country_data

    response["country_data"] = data_list
    loop.run_until_complete(cache.set("all_stats", response, ttl=60 * 15))
    return response


def process_float(value):
    try:
        return float(value)
    except ValueError:
        return value


def calculate_percentage(numerator, denominator):
    try:
        return round((numerator / denominator) * 100, 2)
    except:
        return "NA"


if __name__ == "__main__":
    print(get_data())
