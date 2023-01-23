from django.db import models

class Question(models.Model):
    id = models.IntegerField(primary_key=True)
    # question_text = models.CharField(max_length=200)
    # pub_date = models.DateTimeField('date published')


# class Teacher(models.Model):
#     name = models.CharField(max_length=80)
#     age = models.IntegerField()
    