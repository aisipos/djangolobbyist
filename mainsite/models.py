from django.db import models
from django.contrib.humanize.templatetags.humanize import intcomma
        
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

class Client(models.Model):
    """A client is an organization that is doing lobbying themselves or hiring a "registrant"
       organization to lobby for them.
    """
    client_senate_id          = models.IntegerField(null=True   , blank=True, db_index=True)
    client_name               = models.CharField(max_length=300 , blank=True, null=True, db_index=True)
    client_country            = models.CharField(max_length=150 , blank=True, null=True, db_index=True)
    client_state              = models.CharField(max_length=90  , blank=True, null=True, db_index=True)
    client_ppb_country        = models.CharField(max_length=150 , blank=True, null=True, db_index=True)
    client_ppb_state          = models.CharField(max_length=90  , blank=True, null=True, db_index=True)
    client_description        = models.TextField(blank=True, null=True)
    client_contact_firstname  = models.CharField(max_length=90  , blank=True, null=True)
    client_contact_middlename = models.CharField(max_length=90  , blank=True, null=True)
    client_contact_lastname   = models.CharField(max_length=90  , blank=True, null=True, db_index=True)
    client_contact_suffix     = models.CharField(max_length=12  , blank=True, null=True)
    client_raw_contact_name   = models.CharField(max_length=300 , blank=True, null=True)

    def __repr__(self):
        return '%s' % (self.client_name)
    def __unicode__(self):
        return repr(self)

class Registrant(models.Model):
    """A registrant is an organization who does the lobbying directly."""
    registrant_senate_id      = models.IntegerField(null=True   , blank=True, db_index=True)
    registrant_name           = models.CharField(max_length=300 , blank=True, null=True, db_index=True)
    registrant_description    = models.TextField(blank=True     , null=True)
    registrant_address        = models.CharField(max_length=300 , blank=True, null=True)
    registrant_country        = models.CharField(max_length=90  , blank=True, null=True, db_index=True)
    registrant_ppb_country    = models.CharField(max_length=90  , blank=True, null=True)

    def __repr__(self):
        return '%s' % (self.registrant_name)
    def __unicode__(self):
        return repr(self)


class Issue(models.Model):
    """An Issue is a category that a filing falls into. """
    issue_id       = models.IntegerField(primary_key=True)
    code           = models.CharField(max_length=300, db_index=True)
    specific_issue = models.TextField()

    def __repr__(self):
        return '%s' % (self.code)
    def __unicode__(self):
        return repr(self)

class Filing(models.Model):
    """A filing is one particular lobbying event performed by a lobbyist (as part of a registrant) on behalf of a client. """
    filing_id                 = models.CharField(max_length=108, primary_key=True) #Preserve pk from original table
    filing_period             = models.CharField(max_length=90, null=True, db_index=True)
    filing_date               = models.DateField(null=True, db_index=True)
    filing_amount             = models.IntegerField(null=True, blank=True, db_index=True)
    filing_year               = models.IntegerField(null=True, db_index=True)
    filing_type               = models.CharField(max_length=150, null=True, db_index=True)
    client                    = models.ForeignKey(Client)
    registrant                = models.ForeignKey(Registrant)
    issues                    = models.ManyToManyField(Issue)
    #One filing can have many lobbyists as well
    #One filing can have many issues as well

    def __repr__(self):
        return '%s ($%s on %s by %s)' % (self.filing_id, intcomma(self.filing_amount), self.filing_date, self.registrant)
    def __unicode__(self):
        return repr(self)


class Lobbyist(models.Model):
    """A lobbyist is one particular person working for a registrant"""
    lobbyist_id       = models.IntegerField(primary_key=True) #Preserve pk from original table
    firstname         = models.CharField(max_length=90  , null=True)
    middlename        = models.CharField(max_length=90  , blank=True, null=True)
    lastname          = models.CharField(max_length=90  , null=True)
    suffix            = models.CharField(max_length=12  , blank=True, null=True)
    official_position = models.CharField(max_length=300 , null=True)
    raw_name          = models.CharField(max_length=300 , blank=True, null=True)
    filings           = models.ManyToManyField(Filing)

    def __repr__(self):
        return '%s %s %s' % (self.firstname, self.middlename, self.lastname)
    def __unicode__(self):
        return repr(self)
