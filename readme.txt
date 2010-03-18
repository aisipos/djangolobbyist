Lobbyist is a Django required website to view Senate Office of Public Record (SOPR) data about lobbying.
It is licensed under the GPLv3. See license.txt for details. 
It is currently still very new and under development.

Requirements:
 * Django 1.0.2 or Django 1.1
 * google-chartwrapper (http://code.google.com/p/google-chartwrapper/)
 * django-extensions   (http://github.com/django-extensions/django-extensions)
 * werkzeug (pip install werkzeug)
 * MySQL, python MySQL drivers
 ** A database called django_lobbyist,
 ** This will be created in two stages from the data found at http://data.sunlightlabs.com/sunlightapi/api_lobbyists.sql.gz, which you can do via:
 *** wget http://data.sunlightlabs.com/sunlightapi/api_lobbyists.sql.gz
 **** NOTE:!! As of 3/2010 sunlight labs doesn't have this available. I will contact them for a new location. Contact me for a copy in the meantime.
 *** gunzip api_lobbyists.sql
 *** mysql -u root
 ***  create database lobbyist;
 ***  use lobbyist;
 ***  source api_lobbyists.sql
 ***  create database django_lobbyist
 *** ./manage.py syncdb
 *** mysql -u root < migrate.sql 
 ** Note the last step will take some time. 
 ** modify settings.py if you name this db something else or host it elsewhere than localhost.
 ** settings.py defaults to connecting to DB as root with no password,
    change this if you use different credentials.
 ** As currently bundled, the top level directory needs to be named 'lobbyist'

Overview:
 * In Django parlance, the site is called lobbyist and the app is called mainsite.
 * To run the site, from the root dir run python manage.py runserver
