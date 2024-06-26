# integrations/exceptions.py


class ExchangeRatesAPIException(Exception):
    ERROR_CODES = {
        101: "No API Key was specified or an invalid API Key was specified.",
        102: "The account this API request is coming from is inactive.",
        103: "The requested API endpoint does not exist.",
        104: "The maximum allowed API amount of monthly API requests has been reached.",
        105: "The current subscription plan does not support this API endpoint.",
        106: "The current request did not return any results.",
        201: "An invalid base currency has been entered.",
        202: "One or more invalid symbols have been specified.",
        301: "No date has been specified. [historical]",
        302: "An invalid date has been specified. [historical, convert]",
        403: "No or an invalid amount has been specified. [convert]",
        404: "The requested resource does not exist.",
        501: "No or an invalid timeframe has been specified. [timeseries]",
        502: "No or an invalid 'start_date' has been specified. [timeseries, fluctuation]",
        503: "No or an invalid 'end_date' has been specified. [timeseries, fluctuation]",
        504: "An invalid timeframe has been specified. [timeseries, fluctuation]",
        505: "The specified timeframe is too long, exceeding 365 days. [timeseries, fluctuation]",
    }

    def __init__(self, error_code):
        self.error_code = error_code
        self.message = self.ERROR_CODES.get(error_code, "An unknown error occurred.")
        super().__init__(self.message)
