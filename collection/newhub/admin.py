from django.contrib import admin

from .models import Disease, Symptom, DiseaseLink, User, UserLog, Property, Value

class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User',             {'fields': ['user_name']}),
        ('User information', {'fields': ['user_email','user_organization','is_related','is_doctor'], 'classes': ['collapse']}),
    ]
    list_display = ('user_name','user_email','user_organization','is_related','is_doctor','add_at')

admin.site.register(Disease)
admin.site.register(Symptom)
admin.site.register(DiseaseLink)
admin.site.register(User, UserAdmin)
admin.site.register(UserLog)
admin.site.register(Value)
admin.site.register(Property)

# Register your models here.