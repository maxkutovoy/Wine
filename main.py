import collections
import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_year_word(age):
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
    grouped_drinks = collections.defaultdict(list)
    for drink in drinks:
        grouped_drinks[drink['Категория']].append(drink)
    sorted_drinks = dict(sorted(grouped_drinks.items()))

    today_date = datetime.datetime.today()
    winery_foundation_year = 1920
    winary_age = today_date.year - winery_foundation_year

    rendered_page = template.render(
        all_drinks=sorted_drinks,
        winary_age=winary_age,
        age_word=get_year_word(winary_age),
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
