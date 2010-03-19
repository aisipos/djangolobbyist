from django import template
from django.template.defaultfilters import stringfilter
from urllib           import quote, unquote

register = template.Library()

@register.filter
@stringfilter
def make_key(s):
    """Need to make a "key" field to produce links with. We'll use code, url encoded with slashes turned to dashes"""
    return quote(s.replace('/','-').lower())

@register.filter
@stringfilter
def unquote_key(s):
    """Need to make a "key" field to produce links with. We'll use code, url encoded with slashes turned to dashes"""
    return unquote(s).upper().replace('-','/')

@register.filter
@stringfilter
def filingPdfLink(filing_id):
    "Given a filing id, generate a link to it's PDF from soprweb.senate.gov"
    return "http://soprweb.senate.gov/index.cfm?event=getFilingDetails&filingID=%s" % (filing_id)
