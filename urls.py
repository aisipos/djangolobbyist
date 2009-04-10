from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$'            ,'lobbyist.mainsite.views.index', name = 'home'),
                       url(r'^issues?/$'                          ,'lobbyist.mainsite.views.issues',          name = 'issue'),
                       url(r'^issues?/(?P<code>.+?)/$'        ,'lobbyist.mainsite.views.issue_detail',    name = 'issue_detail'),
                       url(r'^lobbyists?/(?P<first_name>.*?)/(?P<last_name>.*?)/$'  ,'lobbyist.mainsite.views.lobbyist_detail', name = 'lobbyist_detail'),
                       url(r'^lobbyists?/$'                          ,'lobbyist.mainsite.views.lobbyists',       name = 'lobbyist'),
                       url(r'^clients?/$'                            ,'lobbyist.mainsite.views.clients',          name = 'client'),
                       url(r'^clients?/(?P<client_id>\d+)/$'         ,'lobbyist.mainsite.views.client_detail',    name = 'client_detail'),
                       url(r'^registrants?/$'                        ,'lobbyist.mainsite.views.registrants',      name = 'registrant'),
                       url(r'^registrants?/(?P<registrant_id>\d+)/$' ,'lobbyist.mainsite.views.registrant_detail',name = 'registrant_detail'),
                       
    # Example:
    # (r'^lobbyist/', include('lobbywatch.foo.urls')),
                       

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
)
