from django.contrib import admin

from voting_system.models import *

admin.site.register(Vote)
admin.site.register(Voting)
admin.site.register(Option)
