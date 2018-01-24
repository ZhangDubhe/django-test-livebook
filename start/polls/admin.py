from django.contrib import admin

from .models import Diseases, Symptom, DiseaseLink, User, UserLink, Property, Value

class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User',             {'fields': ['user_name']}),
        ('User information', {'fields': ['user_email','user_organization','is_related','is_doctor'], 'classes': ['collapse']}),
    ]
    list_display = ('user_name','user_email','user_organization','is_related','is_doctor','add_at')

admin.site.register(Diseases)
admin.site.register(Symptom)
admin.site.register(DiseaseLink)
admin.site.register(User, UserAdmin)
admin.site.register(UserLink)
admin.site.register(Value)
admin.site.register(Property)

# Register your models here.
