## Introduction

This project implements a REST API for converting currencies using real-time exchange rates. It allows users to convert between different currencies and records each transaction for future reference. The API supports BRL, USD, EUR, and JPY currencies.
It also allows the user to fetch transactions.

### Main Technologies in This Project
- **Python**
- **Django**: Django framework
- **Django REST Framework**: APIs
- **Django REST Framework SimpleJWT**: Authentication
- **Swagger**: To document the API
- **Sentry**: To store logs
- **Docker and Docker Compose**: To make it easier to run the project locally
- **Postgres**: Database
- **Pre-Commit**: Pre commit of github with black, isort and flake
- **Github Actions**: For pipeline
- **Exchange Rate API Integration**: To get the real-time currency

### Key Features
- **Users**: Endpoint to register new users and list users.
- **Currency Conversion**: Logged-in users can request to convert between BRL, USD, EUR, and JPY.
- **Real-time Exchange Rates**: Fetch real-time exchange rates from an external API. Since we are using the free tier of Exchange Rates API, which only provides the current currency rates in EUR, we use this data to convert to other currencies.
- **Transaction Recording**: Record each conversion transaction in the database.
- **Transaction History**: Retrieve the transaction history for a user.
- **Logging**: Logging it's being stored in Sentry in production and are display in the console on local environment.
- **Error Handling**: The errors are mostly treated by Django and Django REST Framework automatically. For the integration with Exchange Rates API, an `ExchangeRatesAPIException` was created to handle errors accordingly and give the client a better response.

# How to run
Rename the file src/api/core/local.example.env to src/api/core/local.env

`$ python3.11 -m venv venv`
`$ source venv/bin/activate`
`$ make install-req`
`$ make install-dev-req`
`$ make install-test-req`
Change db at DATABASE_URL var at local.env to localhost

`$ docker-compose up -d db`
`$ python src/manage.py migrate`
`$ python src/manage.py collectstatic`
`$ make test`
`$ python src/manage.py createsuperuser`
`$ make run`
Access http://localhost:8000/admin/

Running with Docker
`docker-compose up -d`
Access http://localhost:8000/admin/


## Playing with the API

In order to access the API documentation, you can visit `https://currencyconversor.onrender.com/swagger/`.

### Steps to Use the API

1. **Create a User**: 
   - Go to the user registration API: `https://currencyconversor.onrender.com/swagger/#/users/users_create`.
   - The username must be unique.

2. **Log In**:
   - Go to the token endpoint: `https://currencyconversor.onrender.com/swagger/#/token/token_create`.
   - Enter your username and password to obtain an access token.
   - Copy the access token.

3. **Authorize**:
   - In the swagger-ui, click the `Authorize` button in the top right.
   - Paste the access token you copied in the previous step.

4. **Create a Transaction**:
   - Convert a currency to another (e.g., USD to BRL) using the transaction creation API: `https://currencyconversor.onrender.com/swagger/#/transactions/transactions_create`.

5. **Get Transactions**:
   - Retrieve transactions filtered by your user using the transaction listing API: `https://currencyconversor.onrender.com/swagger/#/transactions/transactions_list`.


## Discussion

There are a few key points that I would discuss in a real scenario to think more deeply about the architecture of this project.

1. **Exchange Rate API Request Limit**
   - The current limit per month is 250 requests, which is quite low. How many requests would be enough to make this API reliable at all times? In a scenario where we consume all our requests in a month before the end of the month, this would be a critical design failure.
   - Ideally, we wouldn't need to worry about the request limit per month because the project could pay for a higher tier. If this is not feasible, a caching strategy could be implemented to avoid exhausting the request limit before the end of the month. This is a tradeoff because we would have to accept not being "real-time," as there would be a delay in the currency information for the hours we get the information from the cache instead of the API integration.

2. **List of Transactions of Other Users**
   - Should we have roles in this project, like managers and normal users? If so, perhaps a manager could see the list of transactions of all users, while 'normal' users could only see their own list of transactions.

3. **User unique**
   - Here I'm using the username as unique but I think the best to authenticate the app would be via OAuth2 or if 
   a JWT token is really necessary, then the email should be the key to validate the user.
