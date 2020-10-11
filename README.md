# placement-site-crawler

This script extracts new announcements and jobs from the placement website after every set interval of time and sends email, Whatsapp message to the configured receivers.

## How to run?
#
`app.py` expects these environment variables:

EMAIL, PASSWORD - The login credentials for placement site.
TIME_INTERVAL - The time interval between two successive scraping
#
`notifications.py` expects these environmental variables:

PHONE_NO - The phone number to which you want to send whatsapp message.

WHATSAPP_API_KEY - Secret API key to communicate with whatsapp (Follow [this](https://www.callmebot.com/blog/free-api-whatsapp-messages/) blog).

SENDGRID_API_KEY - Secret key for sending email (Generate from [here](https://sendgrid.com/solutions/email-api/)).
#
First install the required packages: 
```sh
pip install -r requirements.txt
```
To run the script:
```sh
python app.py
```

## Deploying on Heroku
To deploy on heroku we need to add these 2 buildpacks in our heroku app's settings:

* [heroku-buildpack-google-chrome](https://github.com/heroku/heroku-buildpack-google-chrome)

* [heroku-buildpack-chromedriver](https://github.com/heroku/heroku-buildpack-chromedriver)

Add these 2 additional environment variables in app's configuration:

1. GOOGLE_CHROME_BIN - /app/.apt/usr/bin/google-chrome
2. CHROMEDRIVER_PATH - /app/.chromedriver/bin/chromedriver

After that create a `Procfile` with the worker process containing the command to run the script
```
worker: python app.py
```