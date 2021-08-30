"""Script for scraping sales prices from boliga.dk."""

from typing import List, TypedDict
import argparse
import urllib.parse
import re
import logging
from pathlib import Path

import requests
import bs4  # type: ignore
import pandas  # type: ignore


class Row(TypedDict):
    """A row of sales price data."""

    address: str
    zip: str
    price: float
    date: str
    rooms: str
    m2: str
    built: str
    m2_price: float


class NoSoldListError(Exception):
    """Error used when the boliga response contains no sold list."""

    pass


address_pattern = (r'(?P<street>[a-zA-ZæøåÆØÅ ]+) '
                   r'(?P<number>\d+[A-Z]?) '
                   r'(?P<zip>\d+) '
                   r'(?P<city>[a-zA-ZæøåÆØÅ ]+)')


def scrape_prices(soup: bs4.BeautifulSoup) -> List[Row]:
    """Scrape all sales prices from the sold table in a boliga response.."""
    if not soup.find_all('app-sold-list-table'):
        raise NoSoldListError()
    table = soup.find_all('app-sold-list-table')[0].table

    rows = []
    for row in table.find_all('tr'):
        columns = row.find_all('td')

        street   = scrape_street(columns)
        zip_code = scrape_zip_code(columns)
        price    = scrape_price(columns)
        date     = scrape_date(columns)
        rooms    = scrape_rooms(columns)
        area     = scrape_area(columns)
        year     = scrape_year(columns)

        rows.append(Row({
            'address' : street,
            'zip'     : zip_code,
            'price'   : float(price),
            'date'    : date,
            'rooms'   : rooms,
            'm2'      : area,
            'built'   : year,
            'm2_price': float(price) / int(area)
        }))
    return rows


def scrape_year(columns: bs4.element.ResultSet) -> str:
    """Scrape the build year from a row in the boliga sold table."""
    year = columns[5].find_all('span', {'class': None})[0].text.strip()
    return year


def scrape_area(columns: bs4.element.ResultSet) -> str:
    """Scrape the area in m2 from a row in the boliga sold table."""
    area = columns[3].find('span').text.strip()
    m = re.match(r'\d+', area)
    if m is None:
        raise ValueError(f'Malformed area: {area}')
    area = m[0]
    return area


def scrape_rooms(columns: bs4.element.ResultSet) -> str:
    """Scrape the no. of rooms from a row in the boliga sold table."""
    rooms = columns[4].text.strip()
    return rooms


def scrape_date(columns: bs4.element.ResultSet) -> str:
    """Scrape the sales date from a row in the boliga sold table."""
    date = columns[2].find_all(
        'span',
        {'class': 'text-nowrap'}
    )[0].text.strip()
    return date


def scrape_price(columns: bs4.element.ResultSet) -> str:
    """Scrape the sales price from a row in the boliga sold table."""
    price = columns[1].find_all(
        'span',
        {'class': 'text-nowrap'}
    )[0].text.replace(
        '\xa0',
        ''
    ).replace(
        '.',
        ''
    ).replace(
        'kr',
        ''
    ).strip()
    return price


def match_address(columns: bs4.element.ResultSet) -> re.Match:
    """Scrape the address from a sold table row and apply address regex."""
    address = columns[0].find(attrs={'data-gtm': 'sales_address'}).text.strip()
    m = re.match(address_pattern, address)
    if m is None:
        raise ValueError(f'Malformed address: {address}')
    return m


def scrape_street(columns: bs4.element.ResultSet) -> str:
    """Scrape the street name and no. from a row in the boliga sold table."""
    m = match_address(columns)
    street = f'{m.group("street")} {m.group("number")}'
    return street


def scrape_zip_code(columns: bs4.element.ResultSet) -> str:
    """Scrape the zip code from a row in the boliga sold table."""
    m = match_address(columns)
    zip_code = m.group('zip')
    return zip_code


def make_request(street: str, zip_code: str) -> bs4.BeautifulSoup:
    """Make request to boliga.dk."""
    url = (f'https://www.boliga.dk/salg/'
           f'resultater?searchTab=1&propertyType=1&zipcodeFrom={zip_code}&'
           f'zipcodeTo={zip_code}&street={urllib.parse.quote_plus(street)}&'
           f'sort=date-d&page=1')
    response = requests.get(url)
    return bs4.BeautifulSoup(response.text, features="html.parser")


def format_filename(streets_txt: str) -> str:
    """Format the output csv file name."""
    name = Path(streets_txt).stem.lower().replace(' ', '_')
    return f'{name}.csv'


def main(streets_txt: str, zip_code: str) -> None:
    """Entry-point for script."""
    rows = []
    with open(streets_txt) as f:
        streets = f.read().splitlines()
    for street in streets:
        logging.info(f'Scraping {street}')
        soup = make_request(street, zip_code)
        try:
            new_rows = scrape_prices(soup)
            logging.info(f'Got {len(new_rows)} new rows')
            rows.extend(new_rows)
        except NoSoldListError:
            logging.error(f'No sold list found for {street}')
            continue
    filename = format_filename(streets_txt)
    logging.info(f'Saving {filename} with a total of {len(rows)} rows')
    pandas.DataFrame(rows).to_csv(filename, index=False)


if __name__ == '__main__':
    logformat = '%(filename)s:%(lineno)-3s :: %(levelname)-8s :: %(message)s'
    logging.basicConfig(format=logformat)
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('streets_txt')
    parser.add_argument('zip')

    args = parser.parse_args()

    main(args.streets_txt, args.zip)
