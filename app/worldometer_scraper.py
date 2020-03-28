import requests
from bs4 import BeautifulSoup

data_pos = {
    0: "country_name",
    1: "total_cases",
    2: "new_cases",
    3: "total_deaths",
    4: "new_deaths",
    5: "total_recovered",
    6: "active_cases",
}


def get_data():
    data = requests.get("https://www.worldometers.info/coronavirus/").text
    soup = BeautifulSoup(data)

    table = soup.find("table", id="main_table_countries_today")
    rows = table.findAll("tr")
    response = {}
    data_list = {}
    for row in rows:
        cols = [c for c in row.find_all("td")]
        country_data = {}
        for index, data in enumerate(cols):
            if data_pos.get(index):
                country_data[data_pos[index]] = data.text.strip().strip("+")
        if country_data.get('country_name'):
            data_list[country_data['country_name'].lower()] = country_data
    response["country_data"] = data_list
    return response


if __name__ == "__main__":
    print(get_data())

