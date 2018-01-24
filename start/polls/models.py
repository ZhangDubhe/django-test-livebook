from django.db import models

#Create your models here.
class Diseases(models.Model):
    disease_name = models.CharField(max_length=250, unique=True)

class Symptom(models.Model):
    symptom_name = models.CharField(max_length=250, unique=True)

class User(models.Model):
    user_name = models.CharField(max_length=250)
    user_email = models.CharField(max_length=250, unique=True)
    user_organization = models.CharField(max_length=250)
    user_password = models.CharField(max_length=250)
    is_related = models.BooleanField()
    is_doctor = models.BooleanField()

class Property(models.Model):
    Property_describe = models.CharField(max_length=250)
    symptom_id = models.ForeignKey(Symptom, on_delete=models.CASCADE )
    count_editor = models.IntegerField()

class Value(models.Model):
    disease_id = models.ForeignKey(Diseases, on_delete=models.CASCADE)
    symptom_id = models.ForeignKey(Symptom, on_delete=models.CASCADE)
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    value_detail = models.CharField(max_length=250)
    count_editor = models.IntegerField()


class DiseaseLink(models.Model):
    disease_id = models.ManyToManyField(Diseases)
    symptom_id = models.ManyToManyField(Symptom)
    count_agree = models.IntegerField()
    count_disagree = models.IntegerField()
    is_valid = models.BooleanField()

class UserLink(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    disease_link_id = models.ManyToManyField(DiseaseLink)
    value_id = models.ForeignKey(Value, on_delete=models.CASCADE)
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    add_at = models.DateField()

