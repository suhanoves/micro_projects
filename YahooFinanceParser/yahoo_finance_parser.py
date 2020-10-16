import requests
from bs4 import BeautifulSoup
import re
import csv
import sys

HOST = "https://finance.yahoo.com/"
URL = "https://finance.yahoo.com/quote/"
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}


def read_tickers_for_parcing():
    # open a file with list of tickers for parcing
    try:
        with open("tickers.txt", "r", encoding='utf-8') as file:
            # del /n symbols from every line, get a list of tickers
            tickers = [ticker.strip() for ticker in file]
        # return a list of tickers
        return tickers
    except FileNotFoundError:
        print("The file 'tickers.txt' was not found.")
        sys.exit()


def get_html(ticker):
    # add ticker for create correct full url
    url = URL + ticker + "/profile"
    # get html from Yahoo Finance
    html = requests.get(url, headers=HEADERS).text
    return html if html else None


def get_company_info(ticker, html):
    try:
        soup = BeautifulSoup(html, "html.parser")

        # get information about company
        company = soup.find('h3', class_='Fz(m) Mb(10px)').text

        description = soup.find('p', class_='Mt(15px) Lh(1.6)').text

        website = soup.select_one('a[href*="http:"]')
        website = website['href'] if website else None

        sector_industry = soup.find('p', class_="D(ib) Va(t)").find_all('span', {'class': "Fw(600)",
                                                                                 'data-reactid': True}, limit=2)
        sector, industry = [i.string for i in sector_industry]

        currency = soup.find(string=re.compile("Currency in USD")).split()[-1]
        market = soup.find(string=re.compile("Currency in USD")).split()[0]

        company_information = {
            'ticker': ticker,
            'company': company,
            'website': website,
            'description': description,
            'sector': sector,
            'industry': industry,
            'market': market,
            'currency': currency,
        }

        return company_information
    except AttributeError:
        return False


def get_companies_info(tickers):
    # create a list for all companies
    companies_info = []

    for ticker in tickers:
        print(f'Parcing {ticker}')
        # get web-page from Yahoo Finance for every ticker
        html = get_html(ticker)
        if html:
            # get company indormation by parsing a webpage
            company_info = get_company_info(ticker, html)
            if company_info:
                # append a company to the companies list
                companies_info.append(company_info)
                continue
        print('\n!!!     ERROR     !!!')
        print(f"Сan't get data on ticker {ticker}.\n")
    return companies_info


def create_csv_file(companies_info):
    with open('companies_info.csv', 'w', encoding='utf-8', newline='') as file:
        fieldnames = list(companies_info[0])
        writer = csv.DictWriter(file, fieldnames=fieldnames, dialect='excel')
        writer.writeheader()
        for company in companies_info:
            writer.writerow(company)
    print('\nCreating *.scv file complete!')


def main():
    # get list of tickers
    tickers = read_tickers_for_parcing()
    # get list of information about companies
    companies_info = get_companies_info(tickers)
    if companies_info:
        # create csv file
        create_csv_file(companies_info)
    else:
        print('\nNo data to save! The file was not saved.')


main()
