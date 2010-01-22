from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',# View Prefix, see http://docs.djangoproject.com/en/dev/topics/http/urls/#the-view-prefix
                       url(r'^$'            ,'lobbyist.mainsite.views.index', name = 'home'),
                       url(r'^issues?/$'                             ,'lobbyist.mainsite.views.issues',          name = 'issue'),
                       url(r'^issues?/(?P<issue_id>.+?)/$'           ,'lobbyist.mainsite.views.issue_detail',    name = 'issue_detail'),
                       url(r'^lobbyists?/(?P<lobbyist_id>.+?)/$'    ,'lobbyist.mainsite.views.lobbyist_detail', name = 'lobbyist_detail'),
                       url(r'^lobbyists?/$'                          ,'lobbyist.mainsite.views.lobbyists',       name = 'lobbyist'),
                       url(r'^clients?/$'                            ,'lobbyist.mainsite.views.clients',          name = 'client'),
                       url(r'^clients?/(?P<client_id>\d+)/$'         ,'lobbyist.mainsite.views.client_detail',    name = 'client_detail'),
                       url(r'^registrants?/$'                        ,'lobbyist.mainsite.views.registrants',      name = 'registrant'),
                       url(r'^registrants?/(?P<registrant_id>\d+)/$' ,'lobbyist.mainsite.views.registrant_detail',name = 'registrant_detail'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
)

#Static files (including CSS) are only served by Django during development. 
#See http://docs.djangoproject.com/en/dev/howto/static-files/i
if settings.DEBUG:
    urlpatterns += patterns('', #Prefix
                       url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
)

# if settings.DEBUG:
#     urlpatterns += patterns('django.views.static',
#     (r'^static/(?P<path>.*)$', 
#         'serve', {
#         'document_root': settings.MEDIA_ROOT,
#         'show_indexes': True }),)

