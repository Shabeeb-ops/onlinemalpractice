from django.db import models
from  django.contrib.auth.models import User
# Create your models here.


class Student_table(models.Model):
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    contact=models.BigIntegerField()
    pin=models.BigIntegerField()
    status=models.CharField(max_length=100,default='pending')

class Staff_table(models.Model):
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)
    name= models.CharField(max_length=100)
    qualification=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    contact=models.BigIntegerField()
    place=models.CharField(max_length=100)

class Subject_table(models.Model):
    subject=models.CharField(max_length=100)
    date=models.DateField()

class Notification_table(models.Model):
    notification=models.CharField(max_length=100)
    date=models.DateField()

class Complaint_table(models.Model):
    STUDENT=models.ForeignKey(Student_table,on_delete=models.CASCADE)
    complaint=models.CharField(max_length=100)
    date=models.DateField()
    reply=models.CharField(max_length=100)

class Feedback_table(models.Model):
    STUDENT=models.ForeignKey(Student_table,on_delete=models.CASCADE)
    feedback=models.CharField(max_length=100)
    date=models.DateField()

class Assign_table(models.Model):
    SUBJECT=models.ForeignKey(Subject_table,on_delete=models.CASCADE)
    STAFF=models.ForeignKey(Staff_table,on_delete=models.CASCADE)

class Studymaterial_table(models.Model):
    STAFF=models.ForeignKey(Staff_table,on_delete=models.CASCADE)
    studymaterial=models.FileField()
    date = models.DateField()

class review_table(models.Model):
    STUDENT= models.ForeignKey(Student_table,on_delete=models.CASCADE)
    review=models.CharField(max_length=100)
    rating=models.FloatField()
    date=models.DateField()

class chat_table(models.Model):
    FROM_ID=models.ForeignKey(User,on_delete=models.CASCADE,related_name='from_id')
    TO_ID=models.ForeignKey(User,on_delete=models.CASCADE,related_name='to_id')
    message=models.CharField(max_length=100)
    date = models.DateField()

class Exam_table(models.Model):
    subject = models.ForeignKey(Subject_table,on_delete = models.CASCADE)
    exam = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()

class question_table(models.Model):
    STAFF=models.ForeignKey(Staff_table,on_delete=models.CASCADE)
    EXAM=models.ForeignKey(Exam_table,on_delete=models.CASCADE)
    question=models.TextField()
    option1=models.TextField()
    option2=models.TextField()
    option3=models.TextField()
    option4=models.TextField()
    answer=models.TextField()

class result_table(models.Model):
    STUDENT=models.ForeignKey(Student_table,on_delete=models.CASCADE)
    QUESTION=models.ForeignKey(question_table,on_delete=models.CASCADE)
    mark = models.IntegerField()

class malpratice(models.Model):
    STUDENT = models.ForeignKey(Student_table, on_delete=models.CASCADE)
    EXAM = models.ForeignKey(Exam_table, on_delete=models.CASCADE)
    QUESTION = models.ForeignKey(question_table, on_delete=models.CASCADE)
    malpratice=models.CharField(max_length=50)
    date=models.DateField()












