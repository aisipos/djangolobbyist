#!/usr/bin/python
import settings
from django.core.management import setup_environ
setup_environ(settings)
from django.db import models
from django.db import connection
from itertools import izip
from mainsite.models import Client,Registrant,Filing,Issue,Lobbyist
import sys

debug = True

def safeStr(obj):
    if(isinstance(obj,unicode)):
        return obj.encode('ascii','replace')
    else:
        return str(obj)
def key(obj):
    """
    Generate a value to key on by concatenation of the all string values in obj.__dict__
    Arguments:
    - `obj`:object whose dict to use
    """
    #return u"".join(unicode(x, errors='ignore') for x in obj.__dict__.values())
    return "".join(safeStr(x) for x in obj.__dict__.values())

def subDict(d, fields):
    """
    Create a subset of a dictionary by specifying a list of keys
    Arguments:
    - `d`: Dictionary to use as superset
    - `fields`: List of keys to use
    """
    return dict((key,d[key]) for key in fields)

def dictFetch(cursor):
    """
    Fetch the rows from a cursor that has run execute() one at a time, returning them as dictionaries
    Arguments:
    - `cursor`: cursor object that has just run execute()
    """
    fields = [x[0] for x in cursor.description]
    while(True):
       row = cursor.fetchone()
       if(row is not None):
           yield dict(izip(fields,row)) 
       else:
            break    
#    return( dict(izip(fields,row)) for row in cursor.fetchall())

def MigrateFilings():
    """Move the DB from lobbyist to Django_lobbyist
    """
    cursor = connection.cursor()
    n=0
    clientKeys     = dict()
    registrantKeys = dict()

    print "Selecting all filings"
    cursor.execute("""
select * 
from lobbyist.lobbyists_filing 
where filing_id is not NULL
""")
    fields = [x[0] for x in cursor.description]
    for row in dictFetch(cursor):        
        #Clients and Registrants appear multiple times in the filings table
        #So keep track of which ones we've seen and only add ones we haven't seen
        client     = Client(    **subDict(row, [x for x in fields if x.startswith('client_')] ))
        clientKey = key(client)
        if(clientKey not in clientKeys):
            client.save()
            if debug: print client.__dict__
            clientKeys[clientKey] = client.pk
        else:
            client.pk = clientKeys[clientKey]
        clientKeys.clear()

        registrant = Registrant(**subDict(row, [x for x in fields if x.startswith('registrant_')] ))        
        registrantKey = key(registrant)
        if(registrantKey not in registrantKeys):
            registrant.save()
            registrantKeys[registrantKey] = registrant.pk
            if debug: print registrant.__dict__
        else:
            registrant.pk = registrantKeys[registrantKey]
        registrantKeys.clear()

        #All filing rows are unique filings
        filing = Filing(        **subDict(row, [x for x in fields if x.startswith('filing_')] ))        
        filing.registrant = registrant
        filing.client     = client
        filing.save()
        if debug: print filing.__dict__
        n += 1
        if (n%1000 == 0): print ".",
        sys.stdout.flush()
    print n


def MigrateIssues():
    """
    Migrate the issues table
    """
    cursor = connection.cursor()

    print "Selecting all issues"
    cursor.execute("""
select * 
from lobbyist.lobbyists_issue 
""")
    for row in dictFetch(cursor):        
        issue = Issue(issue_id = row['id'], code = row['code'], specific_issue = row['specific_issue'])
        
        issue.save()
        try:
            filing = Filing.objects.get(filing_id = row['filing_id'])
            filing.issues.add(issue)
            filing.save()
        except Filing.DoesNotExist:
            print "Warning: issue %s has missing filing_id %s" % (issue.issue_id, row['filing_id'])
        if debug: print issue.__dict__

def MigrateLobbyists():
    """
    Migrate the Lobbyists table
    """
    cursor = connection.cursor()
    print "Selecting all lobbyists"
    cursor.execute("""
select * 
from lobbyist.lobbyists_lobbyist
""")
    lobbyistKeys     = dict()
    for row in dictFetch(cursor):        
        #Lobbyists appear multiple times in the lobbyist table. Many to many relationship to filings
        lobbyist = Lobbyist(lobbyist_id = row['id'], firstname = row['firstname'], middlename=row['middlename'], \
                            lastname = row['lastname'], suffix=row['suffix'], official_position = row['official_position'], \
                            raw_name = row['raw_name'])
        lobbyistKey = key(lobbyist)
        if(lobbyistKey not in lobbyistKeys):
            lobbyist.save()
            lobbyistKeys[lobbyistKey] = lobbyist.pk
        else:
            lobbyist.pk = lobbyistKeys[lobbyistKey]

        try:
            filing = Filing.objects.get(filing_id = row['filing_id'])
            lobbyist.filings = filing
            lobbyist.save()
        except Filing.DoesNotExist:
            print "Warning: lobbyist %s has missing filing_id %s" % (lobbyist.lobbyist_id, row['filing_id'])
        if debug: print lobbyist.__dict__

if __name__ == '__main__':
    MigrateFilings()
    MigrateIssues()
    MigrateLobbyists()
