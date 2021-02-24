from bs4 import BeautifulSoup
import requests as req
import pandas as pd
import string
import time

def url_constructor(where, business_type, page_number):
    """Convert inputs to url compliant text"""
    import urllib
    where, business_type = urllib.parse.quote_plus(where), urllib.parse.quote_plus(business_type)
    url = f"https://www.local.ch/en/q?what={business_type}&where={where}&page={page_number}"
    print( url )
    return url


def pick(card, selector, attribute="text"):
    """Scrape attribute from a card item element (i.e. a business on local.ch) using a specific CSS selector"""
    try:
        el = card.select_one(selector)
        if attribute == "text":
            return el.get_text(separator=' ', strip=1)
        else:
            return el.get(attribute)
    except AttributeError as e:
        return None


def scrape_url(url, destination, business_type):
    """Scrape url based on the input keywords submitted
        destination: str, defaults to ''
        business_type: str, defaults to ''
        Returns a df for one page / url
    """
    soup = BeautifulSoup(req.get(url).content, 'html.parser')
    page_df = pd.concat(
        [pd.Series({tup[0]:pick(card, *tup[1:]) for tup in selectors}).to_frame().T
         for card in soup.select('div.js-entry-card-container')], ignore_index=1)
    page_df['category'] = business_type
    page_df['destination'] = destination
    return page_df


def clean_filename(input_):
    return input_.translate(str.maketrans(' ', '_', string.punctuation)).lower()


# information to scrape
selectors = [
    ('title', "h2.card-info-title", "text"),
    ('address', "div.card-info-address", "text"),
    ('categories_details', "div.card-info-category", "text"),
    ('phone', "a[title='Call']", "href"),
    ('website', "a[title='Website']", "href"),
    ('email', "a[title='E-Mail']", "href")
]


def scraper(destination, business_type, filename, self):
    # first save
    page_df = pd.DataFrame(
        columns=[item[0] for item in selectors] + ['category', 'destination'])
    page_df.to_csv(filename, header=True, index=False)

    # append when scraping each page
    for page_number in range(1, 101):
        self.signals.messaging.emit(f"scrapping page_number: {page_number}")
        self.signals.progress.emit(page_number)
        try:
            url = url_constructor(destination, business_type, page_number)
            page_df = scrape_url(url, destination, business_type)
            page_df.email = page_df.email.str[7:]
            page_df.to_csv(filename, mode='a', header=False, index=False)
        except ValueError as e:
            self.signals.messaging.emit(f'Finished scraping on page {page_number}')
            time.sleep(1.5)
            break
        except Exception as e:
            self.signals.messaging.emit(f'Error occured: {e}')
            raise Exception(e)
        else:
            self.signals.messaging.emit(f'Output saved as {filename}')
    return 0
