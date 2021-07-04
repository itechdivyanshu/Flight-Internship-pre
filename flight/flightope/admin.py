from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(airline)
admin.site.register(city)
admin.site.register(aircraft)
admin.site.register(flights)