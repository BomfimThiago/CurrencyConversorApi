from enum import Enum


class TransactionMessages(Enum):
    CREATE_TRANSACTION_SUCCESSFULLY = "Transaction was created successfully"
    GET_USER_TRANSACTION_SUCCESFULLY = "Get user transactions request was successfull"
    SOURCE_AMOUNT_MUST_BE_POSITIVE = "Source amount must be positive"
