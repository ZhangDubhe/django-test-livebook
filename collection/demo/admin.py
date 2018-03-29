from django.contrib import admin

# Register your models here.

from .models import Disease, Symptom, DiseaseLink, User, UserLog, Property, Value


class UserAdmin(admin.ModelAdmin):
	fieldsets = [
		('User', {'fields': ['user_name']}),
		('User information', {'fields': ['user_email', 'is_admin', 'user_password']}),
	]
	list_display = ('user_name', 'user_email', 'add_at', 'user_password', 'is_admin')


class DiseaseAdmin(admin.ModelAdmin):
	list_display = ('id', 'content_unique_id', 'name', 'concept_type')


class SymptomAdmin(admin.ModelAdmin):
	list_display = ('id', 'content_unique_id', 'symptom_name', 'type')


class PropertyAdmin(admin.ModelAdmin):
	list_display = ('id', 'property_describe', 'symptom', 'count_agree', 'count_disagree', 'is_valid')


class DiseaseLinkAdmin(admin.ModelAdmin):
	list_display = ('id', 'get_disease_name', 'get_symptom_name', 'count_agree', 'count_disagree', 'is_valid')

	def get_symptom_name(self, obj):
		return obj.symptom.symptom_name
	get_symptom_name.short_description = 'Symptom'

	def get_disease_name(self, obj):
		return obj.disease.name
	get_disease_name.short_description = 'Disease'


class ValueAdmin(admin.ModelAdmin):
	list_display = ('id', 'value_detail', 'get_disease_name', 'get_symptom_name', 'get_property_name', 'count_agree', 'count_disagree', 'is_valid')

	def get_symptom_name(self, obj):
		return obj.symptom.symptom_name
	get_symptom_name.short_description = 'Symptom'

	def get_disease_name(self, obj):
		return obj.disease.name
	get_disease_name.short_description = 'Disease'

	def get_property_name(self, obj):
		return obj.property.property_describe
	get_property_name.short_description = 'Property'


class UserLogAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'get_disease_name', 'get_symptom_name', 'get_property', 'value', 'add_at')

	def get_symptom_name(self, obj):
		try:
			name = obj.disease_link.symptom
		except:
			try:
				name = obj.value.symptom
			except:
				try:
					name = obj.property.symptom
				except:
					name = '-'
		return name
	get_symptom_name.short_description = 'Symptom'

	def get_disease_name(self, obj):
		try:
			name = obj.disease_link.disease
		except:
			try:
				name = obj.value.disease
			except:
				name = '-'
		return name
	get_disease_name.short_description = 'Disease'

	def get_property(self, obj):
		try:
			name = obj.value.property
		except:
			try:
				name = obj.property
			except obj.property.DoesNotExist:
				name = '-'
		return name
	get_property.short_description = 'Property'


admin.site.register(Disease, DiseaseAdmin)
admin.site.register(Symptom, SymptomAdmin)
admin.site.register(DiseaseLink, DiseaseLinkAdmin)
admin.site.register(Value, ValueAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(UserLog, UserLogAdmin)
