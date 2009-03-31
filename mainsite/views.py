# Create your views here.

from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response
from urllib import quote, unquote
import mainsite.models as model

top = 20

def dictAdd(d, k,v):
    "Add one more key to a dict"
    d[k] = v
    return d

def make_key(s):
    """Need to make a "key" field to produce links with. We'll use code, url encoded with slashes turned to dashes"""
    return quote(s.replace('/','-').lower())

def unquote_key(s):
    """Need to make a "key" field to produce links with. We'll use code, url encoded with slashes turned to dashes"""
    return unquote(s).upper().replace('-','/')

def index(request):
    return render_to_response("index.html", locals(), context_instance = RequestContext(request))

def issues(request):
    #import pdb
    #pdb.set_trace()
    top_issues_raw = model.issue.get_top(top)
    top_issues = [dictAdd(issue,'key',make_key(issue['code']) )  for issue in top_issues_raw]
    issues_sum = sum(issue['count'] for issue in top_issues)
    return render_to_response("issue/top_issues.html", locals(), context_instance = RequestContext(request))

def issue_detail(request, issue_id):
    #import pdb
    #pdb.set_trace()
    id = unquote_key(issue_id)
    issue = model.issue.get(id)
    return render_to_response("issue/issue.html", locals(), context_instance = RequestContext(request))

def lobbyists(request):
    #import pdb
    #pdb.set_trace()
    top_lobbyists = model.lobbyist.get_top(top)
    return render_to_response("lobbyist/top_lobbyists.html", locals(), context_instance = RequestContext(request))

def lobbyist_detail(request, first_name, last_name):
    first_name = first_name.upper()
    last_name  = last_name.upper()
    #lobbyists = model.lobbyist.get(first_name,last_name) #Will get multiple rows
    lobbyists = model.lobbyist.get_with_filings(first_name, last_name)
    return render_to_response("lobbyist/lobbyist.html", locals(), context_instance = RequestContext(request))

def clients(request):
    top_clients = model.filing.top_clients(top)
    return render_to_response("client/top_clients.html", locals(), context_instance = RequestContext(request))

def client_detail(request):
    raise Exception("You should write this.")

def registrants(request):
    top_registrants = model.filing.top_registrants(top)
    return render_to_response("registrant/top_registrants.html", locals(), context_instance = RequestContext(request))

def registrant_detail(request):
    raise Exception("You should write this.")
