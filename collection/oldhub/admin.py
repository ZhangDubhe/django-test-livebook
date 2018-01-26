from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Disease, Symptom, Property, Value

admin.site.register(Disease)
admin.site.register(Symptom)
admin.site.register(Value)
admin.site.register(Property)

# Register your models here.