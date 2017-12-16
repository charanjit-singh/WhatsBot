from django.contrib import admin
from .models import *

admin.site.register(Admin)
admin.site.register(Bot)
admin.site.register(AdminBot)
# admin.site.register(contact_list)
admin.site.register(Message)
# admin.site.register(ListLinks)
admin.site.register(SyncStatus)
admin.site.register(MessageStatus)
admin.site.register(Document)

# Register your models here.
