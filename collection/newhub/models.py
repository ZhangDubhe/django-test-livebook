from django.db import models

# Create your models here.
# 作为约定，如果一个模型属性是外键引用到另一个模型中的主键时，该属性名自动以 "_id" 作为后缀
#
# 在修改模型后的３步操作:
#
# 修改模型 (in models.py).
# 运行 python manage.py makemigrations 创建对模型变化的迁移数据
# 运行 python manage.py migrate 将迁移应用到数据库中。



class Disease(models.Model):

    disease_name = models.CharField(max_length=250, unique=True)
    def __str__(self):
        # Python 2的话是__unicode__()
        return self.disease_name



class Symptom(models.Model):
    symptom_name = models.CharField(max_length=250, unique=True)
    def __str__(self):
        return self.symptom_name


class User(models.Model):
    user_name = models.CharField(max_length=250)
    user_email = models.CharField(max_length=250, unique=True)
    user_organization = models.CharField(max_length=250)
    user_password = models.CharField(max_length=250)
    is_related = models.BooleanField()
    is_doctor = models.BooleanField()
    add_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user_name + " log in " +  str(self.add_at)


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
    def __str__(self):
        return self.property_describe

class DiseaseLink(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name='diseases', default=1)
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE, related_name='diseases', default=1)
    count_agree = models.IntegerField()
    count_disagree = models.IntegerField()
    is_valid = models.BooleanField()

    class Meta:
        unique_together = ('disease', 'symptom')

    def __str__(self):
        return self.property_describe

class UserLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.ForeignKey(Value, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    DiseaseLink = models.ManyToManyField(DiseaseLink)
    add_at = models.DateTimeField()
    def __str__(self):
        return self.id
