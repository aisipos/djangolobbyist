Lobbyist is a Django required website to view Senate Office of Public Record (SOPR) data about lobbying.
It is licensed under the GPLv3. See license.txt for details. 
It is currently still very new and under development.

Requirements:
 * Django 1.0.2
 * google-chartwrapper (http://code.google.com/p/google-chartwrapper/)
 * MySQL
 ** A database called lobbyist, from the data found at http://data.sunlightlabs.com/sunlightapi/api_lobbyists.sql.gz
 ** modify settings.py if you name this db something else or host it elsewhere than localhost.
 ** settings.py defaults to connecting to DB as root with no password,
    change this if you use different credentials.

Overview:
 * In Django parlance, the site is called lobbyist and the app is called mainsite.
 * To run the site, from the root dir run python manage.py runserver
