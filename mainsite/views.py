# Create your views here.

from django.http      import HttpResponse
from django.template  import Context, loader, RequestContext
from django.shortcuts import render_to_response
from urllib           import quote, unquote
from django.db.models import Count
from django.db        import connection
import mainsite.models as model
from mainsite.models  import Filing,Client,Registrant,Issue,Lobbyist

defaultTop = 20

def index(request):
    n_Filings, n_Clients, n_Registrants, n_Issues, n_Lobbyists  = [obj.objects.count() for obj in Filing,Client,Registrant,Issue,Lobbyist]
    return render_to_response("index.html", locals(), context_instance = RequestContext(request))

def issues(request, top = defaultTop):
    #import pdb
    #pdb.set_trace()
    #Needs index on issue_id in mainsite_filing_issues
    cursor = connection.cursor()
    #TODO: always returns issues with 1 filing, suspect something wrong with migration script
    cursor.execute("SELECT issue_id, COUNT(issue_id) FROM mainsite_filing_issues GROUP BY issue_id ORDER BY COUNT(issue_id) DESC LIMIT %d" % top)
    ids =[x[0] for x in cursor.fetchall()]
    top_issues = Issue.objects.filter(pk__in = ids) #.annotate(count=Count('filing')) #Also slow
    top_issues = sorted(top_issues, key=lambda x: x.filing_set.count(), reverse=True) #Need to resort again
    issues_sum = sum(issue.filing_set.count() for issue in top_issues)
    return render_to_response("issue/top_issues.html", locals(), context_instance = RequestContext(request))

def issue_detail(request, issue_id, top = defaultTop):
    #import pdb
    #pdb.set_trace()
    issue = Issue.objects.get(pk = issue_id)
    filings = issue.filing_set.all()[:defaultTop]
    return render_to_response("issue/issue.html", locals(), context_instance = RequestContext(request))

def lobbyists(request, top = defaultTop):
    #import pdb
    #pdb.set_trace()
    #top_lobbyists = Lobbyist.objects.annotate(num_filings=Count('filings')).order_by('-num_filings')[:5] #
    cursor = connection.cursor()
    #Really needs an index on column lobbyist_id in join table mainsite_lobbyist_filings
    #TODO: always returns lobbyists with 1 filing, suspect something wrong with migration script
    cursor.execute("SELECT lobbyist_id, COUNT(lobbyist_id) FROM mainsite_lobbyist_filings GROUP BY lobbyist_id ORDER BY COUNT(lobbyist_id) DESC LIMIT %d" % top)
    ids =[x[0] for x in cursor.fetchall()]
    top_lobbyists = Lobbyist.objects.filter(pk__in = ids) #.annotate(count=Count('filing')) #Also slow
    top_lobbyists = sorted(top_lobbyists, key=lambda x: x.filings.count(), reverse=True) #Need to resort again
    return render_to_response("lobbyist/top_lobbyists.html", locals(), context_instance = RequestContext(request))

def lobbyist_detail(request, lobbyist_id, top = defaultTop):
    lobbyist = Lobbyist.objects.get(pk = lobbyist_id)
    filings = lobbyist.filings.all()[:defaultTop] #Many to many relationship #TODO: sort by amount
    return render_to_response("lobbyist/lobbyist.html", locals(), context_instance = RequestContext(request))

def clients(request, top = defaultTop):
    #This query is slow
    #clients = Client.objects.annotate(num_filings = Count('filing')).order_by('-num_filings')[:top]
    cursor = connection.cursor()
    cursor.execute("SELECT client_id, COUNT(client_id)  FROM mainsite_filing where client_id != 0 GROUP BY client_id  ORDER BY COUNT(client_id) DESC LIMIT %d" % top)
    ids =[x[0] for x in cursor.fetchall()]
    top_clients = Client.objects.filter(pk__in = ids) #.annotate(count=Count('filing')) #Also slow
    top_clients = sorted(top_clients, key=lambda x: x.filing_set.count(), reverse=True) #Need to resort again
    return render_to_response("client/top_clients.html", locals(), context_instance = RequestContext(request))

def client_detail(request,client_senate_id, top = defaultTop):
    client  = Client.objects.get(pk = client_senate_id)
    filings = client.filing_set.all()[:defaultTop]
    filings_sum = sum( (filing.filing_amount if isinstance(filing.filing_amount, int) else 0) for filing in filings)
    nonzero_sum = filings_sum > 0
    return render_to_response("client/client.html", locals(), context_instance = RequestContext(request))

def registrants(request, top = defaultTop):
    #Slow query
    #top_registrants  = Registrant.objects.annotate(num_filings = Count('filing')).order_by('-num_filings')[:top]
    cursor = connection.cursor()
    cursor.execute("SELECT registrant_id, COUNT(registrant_id)  FROM mainsite_filing where registrant_id != 0 GROUP BY registrant_id  ORDER BY COUNT(registrant_id) DESC LIMIT %d" % top)
    ids =[x[0] for x in cursor.fetchall()]
    top_registrants = Registrant.objects.filter(pk__in = ids) #.annotate(count=Count('filing')) #Also slow
    top_registrants = sorted(top_registrants, key=lambda x: x.filing_set.count(), reverse=True) #Need to resort again
    return render_to_response("registrant/top_registrants.html", locals(), context_instance = RequestContext(request))

def registrant_detail(request, registrant_senate_id, top = defaultTop):
    #top_clients = model.registrant.top_clients(registrant_id, top) #Clients with most filings
    #registrant = Registrant.objects.get(registrant_senate_id = registrant_senate_id) #TODO: senate id's are not unique
    registrant = Registrant.objects.filter(registrant_senate_id = registrant_senate_id)[0]
    return render_to_response("registrant/registrant.html", locals(), context_instance = RequestContext(request))
