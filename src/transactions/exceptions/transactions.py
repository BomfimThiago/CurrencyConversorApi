from rest_framework.exceptions import ValidationError

from transactions.enums.codes import ErrorCodes
from transactions.enums.messages import TransactionMessages


class TransactionSourceAmountMustBePositiveException(ValidationError):
    def __init__(self, detail=TransactionMessages.SOURCE_AMOUNT_MUST_BE_POSITIVE.value):
        super().__init__(detail, ErrorCodes.SOURCE_AMOUNT_MUST_BE_POSITIVE.value)
