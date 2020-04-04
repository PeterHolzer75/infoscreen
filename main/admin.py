from django.contrib import admin

from .models import Address, Message
# Register your models here.

admin.site.register(Address)
admin.site.register(Message)
