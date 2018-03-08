from django.db import models
from django.utils import timezone


# Create your models here.
class UMLS_tgt(models.Model):
    ticket = models.CharField(max_length=250, unique=True)
    add_at = models.DateTimeField('createdAt', auto_now_add=True)

    def __str__(self):
        return self.ticket


class UMLS_st(models.Model):
    ticket = models.CharField(max_length=250, unique=True)
    add_at = models.DateTimeField('createdAt', auto_now_add=True)

    def __str__(self):
        # Python 2的话是__unicode__()
        return self.ticket


class Term(models.Model):
    concept_identifier = models.CharField(max_length=8, null=True)
    name = models.TextField(null=True)
    semantic_type = models.TextField(null=True)
    definition = models.TextField(null=True)
    source = models.CharField(max_length=20, null=True)


class Disease(models.Model):
    content_unique_id = models.CharField(max_length=8, null=True)
    name = models.TextField()
    concept_type = models.CharField(max_length=150,null=True, default="Null")

    def __str__(self):
        return self.name


class Symptom(models.Model):
    content_unique_id = models.CharField(max_length=8, null=True)
    symptom_name = models.TextField()
    type = models.CharField(max_length=150)

    def __str__(self):
        return self.symptom_name


class User(models.Model):
    user_name = models.CharField(max_length=250, unique=True)
    user_email = models.CharField(max_length=250)
    user_password = models.CharField(max_length=250)
    is_admin = models.BooleanField(default=False)
    add_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_name
# delete org and email

class Property(models.Model):
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE )
    property_describe = models.CharField(max_length=250)
    count_editor = models.IntegerField()

    def __str__(self):
        return self.property_describe


class Value(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    value_detail = models.CharField(max_length=250)
    count_editor = models.IntegerField()
    # class Meta:
    #     unique_together = ('disease', 'symptom', 'property')

    def __str__(self):
        return self.value_detail


class DiseaseLink(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name='diseases', default=1)
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE, related_name='diseases', default=1)
    count_agree = models.IntegerField()
    count_disagree = models.IntegerField()
    is_valid = models.BooleanField()

    class Meta:
        unique_together = ('disease', 'symptom')

    def update_valid(self):
        self.is_valid = (self.count_agree > self.count_disagree)
        return self.is_valid

    def __str__(self):
        if self.is_valid:
            valid = "is Valid"
        else:
            valid = "No valid"
        disease_text = "Disease:"+str(self.disease.id)+" "+self.disease.name
        symptom_text = "Symptoms:"+str(self.symptom.id)+" "+self.symptom.symptom_name
        return disease_text+" + "+symptom_text+" - "+valid


class UserLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False, default=1)
    value = models.ForeignKey(Value, on_delete=models.CASCADE,unique=False,  blank=True, null=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE,unique=False, blank=True,null=True)
    disease_link = models.ForeignKey(DiseaseLink, on_delete=models.CASCADE, unique=False,blank=True,null=True)
    add_at = models.DateTimeField('createdAt', auto_now_add=True)

    def __str__(self):
        return self.id



