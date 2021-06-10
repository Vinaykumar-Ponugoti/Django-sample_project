from django.contrib import admin
from .models import Parkslots, Freeslots, Workers

# Register your models here.
admin.site.register(Freeslots)
admin.site.register(Parkslots)
admin.site.register(Workers)