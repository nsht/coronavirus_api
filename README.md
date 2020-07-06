# Coronavirus API

An API built using [fastapi](https://github.com/tiangolo/fastapi) sourcing data from [worldometer](https://www.worldometers.info/coronavirus/) and updated every 15 minutes.

## API docs 
https://corona-api.nishit.xyz/docs

## Stats
https://corona-api.nishit.xyz/stats

## Country specific Data
https://corona-api.nishit.xyz/country/(country_code)

Example: https://corona-api.nishit.xyz/country/in

List of countries can be found here (mostly ISO 3166-1 alpha-2) [stats api result](https://github.com/ryux00/coronavirus_api/blob/master/app/countries.py)


## How to Self Host
To run this yourself, clone the repo and run

``` 
docker-compose up -d
```

Make sure docker and docker-compose are installed.
