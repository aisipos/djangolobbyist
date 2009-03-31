from django.db import models
from django.db import connection

def fix_countstar(s):
    """Return the name of the field, renaming count(*) to count """
    return 'count' if (s == 'count(*)') else s

def fetchall(query, args):
    "Return a list of dicts one per row"
    cursor = connection.cursor()
    cursor.execute( query, args)
    fields = [fix_countstar(desc[0]) for desc in cursor.description ]
    return [dict( zip(fields,row) ) for row in cursor.fetchall()]

def fetchone(query, args):
    "Return a dict representing the row"
    cursor = connection.cursor()
    cursor.execute( query, args)
    fields = [fix_countstar(desc[0]) for desc in cursor.description ]
    return dict( zip(fields,cursor.fetchone()) )


def fetchall_limited(fn):
    """A decorator to take a function that returns a string, and return a function
       that calls the db with this query to return the top n rows
    """
    def new(self, n):        
        cursor = connection.cursor()
        cursor.execute( fn() + " limit %s", [n])
        return cursor.fetchall()
    new.__doc__ = fn.__doc__ #Move docstring to new function
    return new

def fetchall_by_id(fn):
    """A decorator to take a function that returns a string, and return a function
       that calls the db with this query by id.
       The function should have a single %s in it's where by clause
    """
    #n is the id 
    def new(self, id ):        
        cursor = connection.cursor()
        cursor.execute( fn() , [id])
        return cursor.fetchall()
    new.__doc__ = fn.__doc__ #Move docstring to new function
    return new

def fetchone_by_id(fn):
    """A decorator to take a function that returns a string, and return a function
       that calls the db with this query by id.
       The function should have a single %s in it's where by clause
    """
    #n is the id 
    def new(self, id ):        
        cursor = connection.cursor()
        cursor.execute( fn() , [id])
        return cursor.fetchone()
    new.__doc__ = fn.__doc__ #Move docstring to new function
    return new

def group_query(cols, table):
    """Return a query to return unique instances of column(s), and their count from table.
       cols can be a comma separated list."""
    return """select %s ,count(*) from %s
               group by %s 
               order by count(*) desc
               limit %%s
           """ % (cols, table, cols)


class issue(object):
    """Utility functions for the table lobbyists_issue"""
    #Data comes from http://data.sunlightlabs.com/sunlightapi/api_lobbyists.sql.gz
    table = "lobbyists_issue"

    @classmethod
    def get(self, code):
        """Get a single lobbyist by code"""
        return fetchone("select * from %s where code = %%s" % (issue.table), [code])

    @classmethod
    def get_top(self, n):
         """Find the top n rows lobbyists_issue, return a list of name of issue->number of rows"""
         #return "SELECT code,count(*) FROM lobbyists_issue group by code order by count(*) desc"
         return fetchall("""select code ,count(*) from %s
                             group by code 
                             order by count(*) desc
                             limit %%s""" % (issue.table), [n])

    @classmethod
    def get_with_filings(self, code, top):
        """Get lobbyist rows by firstname and lastname. This can return multiple rows"""
        return fetchall("select * from lobbyists_filing as lf right join lobbyists_issue as li on li.filing_id = lf.filing_id where code like %s order by filing_amount desc limit %s", [code,top])

class lobbyist(object):
    """Utility functions for the table lobbyist_lobbyist"""
    #The table lobbyist is not normalized. Each row represents one filing from a lobbyist, and a lobbyist can appear multiple times
    #Each row joins to one row in the lobbyist_filing table
    table = "lobbyists_lobbyist"

    @classmethod
    def get(self, first_name, last_name):
        """Get lobbyist rows by firstname and lastname. This can return multiple rows"""
        return fetchall("select * from %s where firstname = %%s and lastname = %%s" % (lobbyist.table), [first_name,last_name])

    @classmethod
    def get_with_filings(self, first_name, last_name):
        """Get lobbyist rows by firstname and lastname. This can return multiple rows"""
        #TODO: this is slow currently without an index
        return fetchall("select * from lobbyists_filing as lf right join lobbyists_lobbyist as ll on ll.filing_id = lf.filing_id where ll.firstname LIKE %s AND ll.lastname LIKE %s", [first_name,last_name])

    @classmethod
    def get_top(self, n):
        """Find the top n rows lobbyists_lobbyists, return a list of firstname,lastname,count.
           We tell the db to group by (firstname,lastname), which in the case of common names could lump different lobbyists into one.
           Note that many rows have no firstname and lastname.
        """
        return fetchall(group_query("firstname,lastname", "lobbyists_lobbyist"), [n])

class filing(object):
    """ """
    #client_name     the organization who the lobbying is on behalf of
    #registrant_name the lobbying organization itself, which can be the same of client_name
    table = "lobbyists_filing"

    @classmethod
    def top_clients(self, n):
        "Find organizations who have most filings done on their behalf"        
        return fetchall(group_query("client_name", filing.table), [n])

    @classmethod
    def top_registrants(self, n):
        "Find lobbying firms who have most filings"        
        return fetchall(group_query("registrant_name", filing.table), [n]) 

    @classmethod
    def get_filing(self, filing_id):
        "Find a row in filing table given filing_id (which is a GUID string)"
        return fetchone("select * from %s where filing_id = %%S" % filing.table,[filing_id])
