from enum import Enum


class ErrorCodes(Enum):
    NOT_VALID_CURRENCY = "not_valid_currency"
    SOURCE_AMOUNT_MUST_BE_POSITIVE = "source_amount_must_be_positive"
