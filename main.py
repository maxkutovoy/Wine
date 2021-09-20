import collections
import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape


def age_word(age):
    if age % 100 in range(5, 21):
        return 'лет'
    elif age % 10 == 1:
        return 'год'
    elif 2 <= age % 10 <= 4:
        return 'года'


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')
    drinks = pd.read_excel('wine.xlsx').fillna('').to_dict(orient='records')
    sorted_drinks = collections.defaultdict(list)
    for drink in drinks:
        sorted_drinks[drink['Категория']].append(drink)
    sorted_drinks = dict(sorted(sorted_drinks.items()))

    now = datetime.datetime.today()
    winery_foundation = 1920
    winary_age = now.year - winery_foundation

    rendered_page = template.render(
        drinks=sorted_drinks,
        winary_age=winary_age,
        age_word=age_word(winary_age),
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()
