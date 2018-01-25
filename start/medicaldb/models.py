from django.db import models

# Create your models here.
class Disease(models.Model):
    disease_name = models.TextField()
    symptoms = models.ManyToManyField('Symptom', related_name='diseases')

    def __str__(self):
        return self.disease_name


class Property(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Value(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Symptom(models.Model):
    property = models.ForeignKey(Property, related_name='symptoms', on_delete=models.CASCADE )
    value = models.ForeignKey(Value, related_name='symptoms', on_delete=models.CASCADE )

    def get_text(self):
        return '%s > %s' % (self.property, self.value)

    def __str__(self):
        return '%s > %s' % (self.property, self.value)

    class Meta:
        unique_together = ('property', 'value')
