from django.contrib import admin
from mainsite.models  import Filing,Client,Registrant,Issue,Lobbyist

for entity in Filing,Client,Registrant,Issue,Lobbyist:
    admin.site.register(entity)
