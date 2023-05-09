# Парсинг курсов валют с www.cbr.ru

from bs4 import BeautifulSoup
import requests
from decimal import Decimal
import datetime

# Инфа по курсу рубля к этим валютам через Банк России
URL_CBR_XML = "https://www.cbr.ru/currency_base/daily/"


class CurrencyCB:
    """
    Модель курса CurrencyCB с сайта URL_CBR_XML
    """

    def __init__(self, digit_code: str, letters_code: str, units: int, currency_name: str, rate: Decimal) -> None:
        self.digit_code: str = digit_code  # Цифр. код: 036
        self.letters_code: str = letters_code  # Букв. код: AUD
        self.units: int = units  # Количество единиц: 1
        self.currency_name: str = currency_name  # Название валюты: Австралийский доллар
        self.rate: Decimal = rate  # Курс: 54,2589

    def __str__(self) -> str:
        return f"CurrencyCB(digit_code={self.digit_code}, letters_code={self.letters_code}, units={self.units}, currency_name={self.currency_name}, rate={self.rate})"

    def __repr__(self) -> str:
        return f"CurrencyCB(digit_code={self.digit_code}, letters_code={self.letters_code}, units={self.units}, currency_name={self.currency_name}, rate={self.rate})"


def get_currencies_from_cbr() -> tuple[datetime.datetime, list[CurrencyCB]]:
    """
    Возвращает дату действия курса и список моделей CurrencyCB полученных с сайта.
    Например, (datetime.datetime, [CurrencyCB(), CurrencyCB(), ...])

    :return: tuple[datetime.datetime, list[CurrencyCB]]
    """
    page = requests.get(url=URL_CBR_XML, timeout=(5, 5), allow_redirects=True)
    soup = BeautifulSoup(page.text, "html.parser")

    table = soup.findAll('table', class_='data')[0]
    rows = table.findAll('tr')

    column_names = rows[0].findAll('th')
    column_names_valid = ["Цифр. код", "Букв. код", "Единиц", "Валюта", "Курс"]
    for index in range(len(column_names_valid)):
        assert column_names[index].text == column_names_valid[index]

    currencycb_model_list = []
    for row in rows[1:]:
        column = row.findAll('td')
        new_cur = CurrencyCB(
            digit_code=column[0].text,
            letters_code=column[1].text,
            units=int(column[2].text),
            currency_name=column[3].text,
            rate=Decimal(column[4].text.replace(',', '.'))
        )
        currencycb_model_list.append(new_cur)

    # Официальные курсы валют на заданную дату
    date_str = soup.find('button', class_='datepicker-filter_button')
    date = datetime.datetime.strptime(date_str.text, "%d.%m.%Y")

    return date, currencycb_model_list


if __name__ == "__main__":
    curs = get_currencies_from_cbr()
    print(f"{curs=}")
    print("+++++++++")
    print(f"{curs[1][0]}")
