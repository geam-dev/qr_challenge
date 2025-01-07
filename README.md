# QR Challenge

## What is it?

- This project allows you to generate QR codes to redirect users to another URL, enabling you to track analytics such as how many times the code was scanned, from where, and at what time.

## How is the code organized?
#### It is organized into 3 layers

- Presentation Layer:
This layer contains the endpoints accessed by the user.

- Service Layer:
This layer handles the business logic and coordinates interactions with the database.

- Persistence Layer:
This layer contains the models that define the database structure and manages the DB connection.

## Start

- Clone the repository [git clone git@github.com:geam-dev/qr_challenge.git]
- Create a virtual environment [with venv: python -m venv venv]
- Activate the virtual environment [source venv/bin/activate]
- Install requirements [pip install -r requirements.txt]
- Copy `.env.template` into `.env` and edit it with your variables
- Migrate with Alembic [alembic upgrade head]
- Run the server [fastapi run main.py]

## Env

The `.env` file contains the following variables:

- `DB_USER`, `DB_PASS`, `DB_HOST`, `DB_NAME`, `DB_PORT` for the database connection.
- `SECRET_KEY`, `ALGORITHM` for JWT encryption.
- `ACCESS_TOKEN_EXPIRE_MINUTES` for JWT expiration time.
- `APP_URL` **important**. Used to build the URL embedded in the QR code.
- `IP_INFO_ACCESS_TOKEN` for the ipinfo.io service to retrieve information based on an IP address.