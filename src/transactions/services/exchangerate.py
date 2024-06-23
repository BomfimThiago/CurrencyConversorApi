from decimal import Decimal

import requests
import sentry_sdk
from django.conf import settings

from transactions.exceptions.exchangerate import ExchangeRatesAPIException


class ExchangeRatesAPI:
    BASE_URL = settings.EXCHANGERATES_API_URL
    API_KEY = settings.EXCHANGERATES_API_KEY

    @staticmethod
    def get_exchange_rates(base_currency="EUR"):
        url = f"{ExchangeRatesAPI.BASE_URL}?base={base_currency}&access_key={ExchangeRatesAPI.API_KEY}"
        # url = f"{ExchangeRatesAPI.BASE_URL}?base=USD&access_key={ExchangeRatesAPI.API_KEY}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

            data = response.json()
            if "error" in data:
                error_code = data["error"].get("code", "Unknown error code")
                sentry_sdk.capture_exception(ExchangeRatesAPIException(error_code))
                raise ExchangeRatesAPIException(error_code)

            return data["rates"]
        except requests.exceptions.RequestException as e:
            sentry_sdk.capture_exception(e)
            raise ExchangeRatesAPIException(
                "An unknown error occurred while trying to access the ExchangeRates API."
            ) from e

    @staticmethod
    def convert_currency_via_eur(source_currency, target_currency, source_amount, rates):
        api_source_amount = Decimal(rates[source_currency])
        api_target_amount = Decimal(rates[target_currency])

        # Convert source currency to EUR
        if source_currency != "EUR":
            source_amount_in_eur = source_amount / api_source_amount
        else:
            source_amount_in_eur = source_amount

        # Convert EUR to target currency
        if target_currency != "EUR":
            target_amount = source_amount_in_eur * api_target_amount
        else:
            target_amount = source_amount_in_eur

        # Calculate the exchange rate
        if source_currency != "EUR" and target_currency != "EUR":
            exchange_rate = api_target_amount / api_source_amount
        elif source_currency == "EUR":
            exchange_rate = api_target_amount
        else:
            exchange_rate = 1 / api_source_amount

        return round(target_amount, 2), round(exchange_rate, 6)
