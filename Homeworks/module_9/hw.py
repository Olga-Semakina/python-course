import asyncio
import json
import operator
from dataclasses import dataclass

import aiohttp
import requests
from bs4 import BeautifulSoup

base_page_url = 'https://markets.businessinsider.com'


@dataclass
class Company:
    link: str
    code: str
    name: str
    price: float
    p_e: float
    growth: float

    def __init__(self, link: str, name: str, price: float, growth: float):
        self.link = link
        self.name = name
        self.price = price
        self.growth = growth


async def fetch_response(name: str, url: str):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url) as response:
            return (name, await response.text())


async def parse_company_pages(companies: dict):
    tasks = [asyncio.create_task(fetch_response(name, company.link)) for name, company in companies.items()]
    await asyncio.gather(*tasks)
    for task in tasks:
        company_name = task.result()[0]
        company_page_request = task.result()[1]
        company_page = BeautifulSoup(company_page_request, 'html.parser')

        code = company_page.find(attrs={"class": "price-section__category"}).span.get_text().replace(", ", "")
        p_e = float(company_page.find(attrs={"class": "snapshot__header"}, string='P/E Ratio').parent.contents[
                        0].get_text().strip())

        setattr(companies.get(company_name), 'code', code)
        setattr(companies.get(company_name), 'p_e', p_e)


def parse_main_page(page: BeautifulSoup, companies: dict):
    name_index, price_index, growth_index = find_column_indices(page)
    table_body = page.find(attrs={"class": "table__tbody"})

    for row in table_body.findAll('tr'):
        columns = row.find_all('td')

        # get company's name, price and growth in %
        name = columns[name_index].get_text().strip()
        price = float(columns[price_index].next.strip())
        growth = 0
        for elem in columns[growth_index].find_all('span'):
            if ('%' in elem.get_text()):
                growth = float(elem.get_text().replace('%', ''))
        link = columns[name_index].find('a')['href']

        company = Company(base_page_url + link, name, price, growth)
        companies.update({name: company})


def get_most_expensive_companies(companies: dict):
    create_json(companies, "most_expensive_companies.json", 'price', True)


def get_companies_with_lowest_p_e(companies: dict):
    create_json(companies, "lowest_pe_companies.json", 'p_e', False)


def get_companies_with_most_growth(companies: dict):
    create_json(companies, "most_growth_companies.json", 'growth', True)


def create_json(companies: dict, filename: str, attr_sort: str, desc: bool):
    sorted_by_p_e = sorted(companies.values(), key=operator.attrgetter(attr_sort), reverse=desc)[:10]
    json_string = json.dumps([ob.__dict__ for ob in sorted_by_p_e], indent=1)

    with open(filename, "w") as output:
        output.writelines(json_string)


def find_column_indices(page: BeautifulSoup) -> tuple[int, int, int]:
    name_index = 0
    price_index = 0
    growth_index = 0

    table_header = page.find_all(attrs={"class": "table__th"})
    for i, column in enumerate(table_header):
        if ('Name' in column.get_text()):
            name_index = i
        if ('Price' in column.get_text()):
            price_index = i
        if ('1 Year' in column.get_text()):
            growth_index = i
    return (name_index, price_index, growth_index)


async def main():
    request = requests.get(base_page_url + '/index/components/s&p_500')
    page = BeautifulSoup(request.content, 'html.parser')
    companies = {}

    parse_main_page(page, companies)
    await parse_company_pages(companies)

    get_most_expensive_companies(companies)
    get_companies_with_lowest_p_e(companies)
    get_companies_with_most_growth(companies)


asyncio.run(main())
