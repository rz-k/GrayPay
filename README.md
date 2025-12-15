# GrayPay

GrayPay is a simple donation gateway built for users with a ZarinPal account.  
It allows users to receive donations, and each successful payment sends a notification to a Telegram channel.  

This project is specifically designed for **ZarinPal** payment gateway.

---

## Features

- Create a donation gateway for ZarinPal users.  
- Notify a Telegram channel on each successful payment.  
- Configurable minimum payment amount.  
- Easy setup using Docker.

---

## Requirements

- Docker & Docker Compose  
- ZarinPal Merchant account  
- Telegram bot for notifications

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/rz-k/GrayPay.git
cd GrayPay
```
Copy the example environment file:

```bash
cp .env.ini.example .env.ini
```
Edit .env.ini and configure the variables:

Important environment variables:

```ini
[Django settings]
CSRF_TRUSTED_ORIGINS=https://site.com,https://www.site.com
FORCE_SCRIPT_NAME=
BASE_SITE_ADDRESS=https://site.com

[Payment settings]
MINIMUM_PAYMENT=10000  # Minimum donation amount in Tomans
MERCHANT=<zarinpal merchant code>  # Your ZarinPal merchant code
VERIFY_CALLBACK_ROUTE=/verify-transaction/

[Admin user]
DJANGO_SUPERUSER_USERNAME=username
DJANGO_SUPERUSER_EMAIL=username@email.com
DJANGO_SUPERUSER_PASSWORD=password

[Telegram bot]
TOKEN=<telegram bot token>
ACTION_CHANNEL=<channel chant_id channel>

[Optional proxy]
PROXY_SOCKS=
```
## 🧪 Running Tests

GrayPay comes with automated tests written using **pytest**.  
To run all tests, simply execute:

```bash
pytest
```
Make sure your project dependencies are installed before running the tests.


Running the Project
Use Docker Compose to build and run the project:

```bash
docker compose up --build -d
```
The application should now be running and accessible at the URL specified in BASE_SITE_ADDRESS.

Notes
MINIMUM_PAYMENT defines the minimum donation amount (currently 10,000 Tomans).

MERCHANT is your ZarinPal merchant code.

Telegram notifications are sent to the channel specified by ACTION_CHANNEL.

Make sure your Telegram bot token is valid.

