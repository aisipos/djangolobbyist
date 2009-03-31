from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$'            ,'lobbyist.mainsite.views.index', name = 'home'),
                       url(r'^issue/$'                          ,'lobbyist.mainsite.views.issues',          name = 'issue'),
                       url(r'^issue/(?P<issue_id>.+?)/$'        ,'lobbyist.mainsite.views.issue_detail',    name = 'issue_detail'),
                       url(r'^lobbyist/(?P<first_name>.*?)/(?P<last_name>.*?)/$'  ,'lobbyist.mainsite.views.lobbyist_detail', name = 'lobbyist_detail'),
                       url(r'^lobbyist/$'                          ,'lobbyist.mainsite.views.lobbyists',       name = 'lobbyist'),
                       url(r'^client/$'                            ,'lobbyist.mainsite.views.clients',          name = 'client'),
                       url(r'^client/(?P<client_id>\d+)/$'         ,'lobbyist.mainsite.views.client_detail',    name = 'client_detail'),
                       url(r'^registrant/$'                        ,'lobbyist.mainsite.views.registrants',      name = 'registrant'),
                       url(r'^registrant/(?P<registrant_id>\d+)/$' ,'lobbyist.mainsite.views.registrant_detail',name = 'registrant_detail'),
                       
    # Example:
    # (r'^lobbyist/', include('lobbywatch.foo.urls')),
                       

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
)
