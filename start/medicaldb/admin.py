from django.contrib import admin

# Register your models here.
from .models import Disease, Symptom, Property, Value
admin.site.register(Disease)
admin.site.register(Symptom)
admin.site.register(Value)
admin.site.register(Property)