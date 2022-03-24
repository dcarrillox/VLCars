from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import time




def get_n_pages_autocasion(soup):
    lis = soup.find_all("li")
    for li in lis:
        if li.getText().startswith("Página "):
            n_pages = int(li.getText().split(" ")[-1])
    return n_pages


def format_int(string):
    without_symbols = string.replace(".", "").replace("€", "").replace("cv", "").replace("km", "").strip()
    return int(without_symbols)


class AutocasionOnlineCar:
    cars_online = 0

    def __init__(self, soup):
        self.soup = soup # soup object with a separate car
        self.power = str() # init power since some of them don't have this
        self.gear = str() # init gear since some of them don't have this

    def get_brand_model_desc(self):
        raw_text = self.soup.find("h2", itemprop="name").getText().strip()
        # assume brand is the first word of the tittle. Set it lowercase
        self.brand = raw_text.split(" ")[0].lower()
        # assume model is the second word of the tittle. Set it lowercase
        self.model = raw_text.split(" ")[1].lower() if len(raw_text.split(" ")) > 1 else ""
        # extra description
        self.description = " ".join(raw_text.split(" ")[2:]).lower() if len(raw_text.split(" ")) > 2 else ""

    def get_price(self):
        raw_span = self.soup.find_all("span", ["price"])[0]
        span_text = raw_span.getText()
        price = format_int(span_text)
        self.price = price


    def get_car_stats(self):
        for li in self.soup.find_all("li"):
            text = li.getText()
            if text.startswith("Provincia: "):
                self.province = text.replace("Provincia: ", "").lower()
            if text.startswith("Matriculación: "):
                self.age = format_int(text.replace("Matriculación: ", ""))
            if text.startswith("Combustible: "):
                self.fuel = text.replace("Combustible: ", "").lower()
            if text.startswith("Kilómetros: "):
                self.km = format_int(text.replace("Kilómetros: ", ""))
            if text.startswith("Cambio: "):
                self.gear = text.replace("Cambio: ", "").lower()
            if text.startswith("Potencia: "):
                self.power = format_int(text.replace("Potencia: ", ""))


    def get_car_url_hash(self):
        href = self.soup.find("a")["href"]
        self.href = href
        car_url = "https://www.autocasion.com/" + href
        self.url = car_url
        # create a hash for the car
        self.hash = hash(href)


def parse_autocasion_page(soup, timestamp):
    # look for articles blocks with "anuncio" in its class. Each of these entries represents a car advert
    articles = soup.find_all("article", ["anuncio"])

    # iterate the article entries and get the values of the cars. One car per article entry.
    parsed_page = list()
    for article in articles:
        car = AutocasionOnlineCar(article)
        car.get_brand_model_desc()
        car.get_price()
        car.get_car_stats()
        car.get_car_url_hash()

        parsed_page.append([car.href,
                               car.brand,
                               car.model,
                               car.age,
                               car.km,
                               car.price,
                               car.power,
                               car.province,
                               car.fuel,
                               car.gear,
                               car.description,
                               car.url,
                               timestamp,
                               "autocasion"])

    return parsed_page


def query_online_autocasion(target_province):
    # timestamp the online query cars
    timestamp = time.strftime('%Y-%m-%d')

    base_url = f"https://www.autocasion.com/coches-segunda-mano/{target_province}"
    page = requests.get(base_url)
    soup = BeautifulSoup(page.content, "html.parser")

    # get number of pages given by the query province
    n_pages = get_n_pages_autocasion(soup)
    n_pages = 1
    print(f"\nQuerying www.autocasion.com with '{target_province}', {n_pages} pages")
    time.sleep(1)

    parsed_pages = list()
    # iterate the pages
    for i in tqdm(range(1, n_pages + 1)):  # n_pages+1
        page = f"?page={i}"
        page_url = base_url + page

        page = requests.get(page_url)
        soup = BeautifulSoup(page.content, "html.parser")

        # parse the html page
        parsed_pages += parse_autocasion_page(soup, timestamp)

    return parsed_pages





