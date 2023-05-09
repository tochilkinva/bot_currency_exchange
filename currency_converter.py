# Конвертер валют
# TODO Обновлять кусы валют 1 раз в час по расписанию, а не по запросу

from decimal import ROUND_UP, Decimal, InvalidOperation
from cbr_cur_parser import get_currencies_from_cbr
import datetime

# Текущий курс валют
CUR_RATES = {
    # ("USD", "RUB"): Decimal(76.8207),  # Для примера
    # ("RUB", "USD"): Decimal(0.01302),
    # ("USD", "VND"): Decimal(23586.6000),
}

# Список существующих кодов валют
CUR_CODES = {
    "AED": "Дирхам(ОАЭ)",
    "AFN": "Афгани",
    "ALL": "Лек",
    "KMF": "Коморский франк",
    "AMD": "Армянский драм",
    "ANG": "Нидерландский антильский гульден",
    "AOA": "Кванза",
    "ARS": "Аргентинское песо",
    "AUD": "Австралийский доллар",
    "AWG": "Арубанский флорин",
    "AZN": "Азербайджанский манат",
    "BAM": "Конвертируемая марка",
    "BBD": "Барбадосский доллар",
    "BDT": "Така",
    "BGN": "Болгарский лев",
    "BHD": "Бахрейнский динар",
    "BIF": "Бурундийский франк",
    "BMD": "Бермудский доллар",
    "BND": "Брунейский доллар",
    "BOB": "Боливиано",
    "BRL": "Бразильский реал",
    "BSD": "Багамский доллар",
    "BTN": "Нгултрум",
    "BWP": "Пула",
    "BYN": "Белорусский рубль",
    "BYR": "Белорусский рубль",
    "BZD": "Белизский доллар",
    "CAD": "Канадский доллар",
    "CDF": "Конголезский франк",
    "CHF": "Швейцарский франк",
    "CLP": "Чилийское песо",
    "CNY": "Юань",
    "COP": "Колумбийское песо",
    "COU": "Единица реальной стоимости",
    "CRC": "Костариканский колон",
    "CUC": "Конвертируемое песо",
    "CUP": "Кубинское песо",
    "CVE": "Эскудо Кабо-Верде",
    "CZK": "Чешская крона",
    "DJF": "Франк Джибути",
    "DKK": "Датская крона",
    "DOP": "Доминиканское песо",
    "DZD": "Алжирский динар",
    "LAK": "Лаосский кип",
    "LTL": "Литовский лит",
    "MRO": "Угия",
    "VES": "Боливар Соберано",
    "MRU": "Угия",
    "STD": "Добра",
    "STN": "Добра",
    "VEF": "Боливар",
    "EGP": "Египетский фунт",
    "ERN": "Накфа",
    "ETB": "Эфиопский быр",
    "EUR": "Евро",
    "FJD": "Доллар Фиджи",
    "FKP": "Фунт Фолклендских островов",
    "GBP": "Фунт стерлингов",
    "GEL": "Лари",
    "GHS": "Ганский седи",
    "GIP": "Гибралтарский фунт",
    "GMD": "Даласи",
    "GNF": "Гвинейский франк",
    "GTQ": "Кетсаль",
    "GYD": "Гайанский доллар",
    "HKD": "Гонконгский доллар",
    "HNL": "Лемпира",
    "HRK": "Куна",
    "HTG": "Гурд",
    "HUF": "Форинт",
    "IDR": "Рупия",
    "ILS": "Новый израильский шекель",
    "INR": "Индийская рупия",
    "IQD": "Иракский динар",
    "IRR": "Иранский риал",
    "ISK": "Исландская крона",
    "JMD": "Ямайский доллар",
    "JOD": "Иорданский динар",
    "JPY": "Иена",
    "KES": "Кенийский шиллинг",
    "KGS": "Сом",
    "KHR": "Риель",
    "KPW": "Северокорейская вона",
    "KRW": "Вона",
    "KWD": "Кувейтский динар",
    "KYD": "Доллар Островов Кайман",
    "KZT": "Тенге",
    "LBP": "Ливанский фунт",
    "LKR": "Шри-Ланкийская рупия",
    "LRD": "Либерийский доллар",
    "LSL": "Лоти",
    "LVL": "Латвийский лат",
    "LYD": "Ливийский динар",
    "MAD": "Марокканский дирхам",
    "MDL": "Молдавский лей",
    "MGA": "Малагасийский ариари",
    "MKD": "Денар",
    "MMK": "Кьят",
    "MNT": "Тугрик",
    "MOP": "Патака",
    "MUR": "Маврикийская рупия",
    "MVR": "Руфия",
    "MWK": "Малавийская квача",
    "MXN": "Мексиканское песо",
    "MYR": "Малайзийский ринггит",
    "MZN": "Мозамбикский метикал",
    "NAD": "Доллар Намибии",
    "NGN": "Найра",
    "NIO": "Золотая кордоба",
    "NOK": "Норвежская крона",
    "NPR": "Непальская рупия",
    "NZD": "Новозеландский доллар",
    "OMR": "Оманский риал",
    "PAB": "Бальбоа",
    "PEN": "Соль",
    "PGK": "Кина",
    "PHP": "Филиппинское песо",
    "PKR": "Пакистанская рупия",
    "PLN": "Злотый",
    "PYG": "Гуарани",
    "QAR": "Катарский риал",
    "RON": "Румынский лей",
    "RSD": "Сербский динар",
    "RUB": "Российский рубль",
    "RWF": "Франк Руанды",
    "SAR": "Саудовский риял",
    "SBD": "Доллар Соломоновых Островов",
    "SCR": "Сейшельская рупия",
    "SDG": "Суданский фунт",
    "SEK": "Шведская крона",
    "SGD": "Сингапурский доллар",
    "SHP": "Фунт Святой Елены",
    "SLL": "Леоне",
    "SOS": "Сомалийский шиллинг",
    "SRD": "Суринамский доллар",
    "SSP": "Южносуданский фунт",
    "SVC": "Сальвадорский колон",
    "SYP": "Сирийский фунт",
    "SZL": "Лилангени",
    "THB": "Бат",
    "TJS": "Сомони",
    "TMT": "Новый туркменский манат",
    "TND": "Тунисский динар",
    "TOP": "Паанга",
    "TRY": "Турецкая лира",
    "TTD": "Доллар Тринидада и Тобаго",
    "TWD": "Новый тайваньский доллар",
    "TZS": "Танзанийский шиллинг",
    "UAH": "Гривна",
    "UGX": "Угандийский шиллинг",
    "USD": "Доллар США",
    "UYI": "Уругвайское песо в индексированных единицах",
    "UYU": "Уругвайское песо",
    "UZS": "Узбекский сум",
    "VND": "Донг",
    "VUV": "Вату",
    "WST": "Тала",
    "XAF": "Франк КФАВЕАС",
    "XCD": "Восточно-карибский доллар",
    "XDR": "СДР(специальные права заимствования)",
    "XOF": "Франк КФАВСЕАО",
    "XPF": "Франк КФП",
    "YER": "Йеменский риал",
    "ZAR": "Рэнд",
    "ZMW": "Замбийская квача",
    "ZWL": "Доллар Зимбабве",
}


def valid_rate(rate: str) -> Decimal:
    """
    Возвращает курс в виде Decimal.
    Если указан обратный курс, то переводит его 1/76.82 в 0.01302

    :param rate: str
    :return: Decimal
    """
    rate = rate.replace(',', '.') if ',' in rate else rate

    # Если указан курс 1/76.82
    if "/" in rate:
        rate = rate.split("/")[1]
        try:
            rate = Decimal(rate)
        except InvalidOperation:
            raise Exception("Ошибка в курсе. Введите курс в виде 999.99 или 999,99")

        return 1/rate

    try:
        rate = Decimal(rate)
    except InvalidOperation:
        raise Exception("Ошибка в курсе. Введите курс в виде 999.99 или 999,99")

    return rate


def validate_input(text: str) -> tuple[Decimal, str, str, Decimal] | tuple[Decimal, str, str, None]:
    """
    Валидирует входные данные и преобразует к нужным типам данных.
    Возвращает: number, cur_currency, desired_currency, rate

    :param text: str
    :return: tuple[Decimal, str, str, Decimal] | tuple[Decimal, str, str, None]
    """

    # Распарсили входные данные
    text_list = text.split(" ")
    text_list_len = len(text_list)
    if text_list_len not in [3, 4]:
        raise Exception("Введите сумму, текущую валюту, необходимую валюту и опционально курс необходимой валюты к текущей. Например, 100 RUB USD 75.12")

    if text_list_len == 3:
        number, cur_currency, desired_currency = text.split(" ")
        rate = None
    else:
        number, cur_currency, desired_currency, rate = text.split(" ")

    # Подготовили числа
    number = number.replace(',', '.') if ',' in number else number
    try:
        number = Decimal(number)
    except InvalidOperation:
        raise Exception("Ошибка в сумме. Введите сумму в виде 999 или 999.99 или 999,99")

    if rate:
        rate = valid_rate(rate)

    # Проверили буквенный код валюты
    cur_currency = cur_currency.upper()
    desired_currency = desired_currency.upper()
    if (cur_currency or desired_currency) not in CUR_CODES.keys():
        raise Exception("Ошибка в коде курса. Введите код в виде USD, rub, Eur")

    # print(f"{number=} {cur_currency=} {desired_currency=} {rate=}")
    return number, cur_currency, desired_currency, rate


def get_rate(cur_currency: str, desired_currency: str) -> Decimal:
    """
    Возвращает курс из словаря или вычисляет через кросс курс

    :param cur_currency: str
    :param desired_currency: str
    :return: Decimal
    """
    # Возвращаем курс из словаря
    rate = CUR_RATES.get((desired_currency, cur_currency))
    if rate:
        # print(f" Возвращаем курс {rate=}")
        return rate

    # Возвращаем обратный курс из словаря
    if rate := CUR_RATES.get((cur_currency, desired_currency)):
        rate = Decimal(1)/rate
        # print(f"Возвращаем обратный курс {rate=}")
        return rate

    # Возвращаем кросс курс через доллар
    cur_currency_rate = CUR_RATES.get(("USD", cur_currency))
    desired_currency_rate = CUR_RATES.get(("USD", desired_currency))

    if not cur_currency_rate or not desired_currency_rate:
        raise Exception("Нет курса для этих валют")

    rate = cur_currency_rate / desired_currency_rate
    # print(f"Возвращаем кросс курс через доллар {rate=}")
    return rate


def add_rate_from_cbr() -> datetime.datetime:
    """
    Добавляет в словарь свежие курсы валют и возвращает дату действия курса.
    """
    cur_date, cur_list = get_currencies_from_cbr()
    for cur in cur_list:
        new_cur_key = (cur.letters_code, "RUB")
        new_cur_value = Decimal(cur.rate / cur.units)
        CUR_RATES.update({new_cur_key: new_cur_value})

    return cur_date


def get_codes() -> str:
    """
    Возвращает список доступных валют и их коды.

    :return: str
    """
    codes_list = []
    cur_date, cur_list = get_currencies_from_cbr()
    for cur in cur_list:
        codes_list.append(f"{cur.letters_code} {cur.currency_name}")
    before_text = "Список доступных курсов валют и их кодов по отношению к рублю: \n"
    text = "\n".join(codes_list)
    return f"{before_text}{text}"


def run(in_messege: str) -> str:
    """
    Вычисляет стоимость денег одной валюты в другой валюте.
        in_messege = "10000,0 RUB USD"

        return = "10000.0 Российский рубль = 130.17325 Доллар США при курсе USD/RUB=76.82071"

    С указанием курса
        in_messege = "10000 RUB USD 77.99"  # USD/RUB=77.99

        in_messege = "10000,0 USD RUB /77.99"  # RUB/USD=1/77.99

    :param in_messege: str
    :return: str
    """
    # Получаем последние курсы валют и дату действия курса
    cur_date = add_rate_from_cbr()

    # Входные данные. Валидация и преобразование
    number, cur_currency, desired_currency, rate = validate_input(in_messege)

    # Запрос курса
    if not rate:
        rate = get_rate(cur_currency, desired_currency)

    # Подсчет суммы в нужной валюте
    calculation = number / rate

    # Вывод результата
    result = calculation.quantize(Decimal('.00000'), rounding=ROUND_UP).to_eng_string()
    rate = rate.quantize(Decimal('.00000'), rounding=ROUND_UP).to_eng_string()
    result_str = f"{number} {CUR_CODES[cur_currency]} = {result} {CUR_CODES[desired_currency]} при курсе {desired_currency}/{cur_currency}={rate} на дату {cur_date.date()}"

    return result_str


if __name__ == "__main__":
    # Сообщение от пользователя
    # Формат: сумма, текущая валюта, необходимая валюта
    in_messege = "10000,0 RUB USD"
    # in_messege = "10000,0 USD RUB"
    # in_messege = "10000,0 RUB VND"
    # in_messege = "10000,0 VND RUB"

    # Формат: сумма, текущая валюта, необходимая валюта, курс
    # in_messege = "10000 RUB USD 77.9999"  # USD/RUB=77.9999
    # in_messege = "10000,0 OMR USD 0,3850"

    # Формат: сумма, текущая валюта, необходимая валюта, обратный курс
    # in_messege = "10000,0 USD RUB /76.82071"  # RUB/USD=1/76.82071

    print(f"{in_messege=}")
    result_str = run(in_messege=in_messege)
    print(result_str)
