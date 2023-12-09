from django.db import models

# Create your models here.
class Candidate(models.Model):
    username=models.CharField(max_length=50,primary_key=True)
    password=models.CharField(null=False,max_length=50)
    email=models.CharField(max_length=70,null=False)
    name=models.CharField(null=False,max_length=50)
    test_attempt=models.IntegerField(default=0)
    point=models.FloatField(default=0.0)

class Question(models.Model):
    Qid=models.BigAutoField(primary_key=True,auto_created=True)
    title=models.CharField(max_length=255)
    Question=models.TextField()
    img=models.ImageField(upload_to='Image',blank=True)
    option_a=models.CharField(max_length=255)
    option_b=models.CharField(max_length=255)
    option_c=models.CharField(max_length=255)
    option_d=models.CharField(max_length=255)
    answer=models.CharField(max_length=255)
    explanation=models.TextField(null=True)


class Result(models.Model):
    resultid=models.BigAutoField(primary_key=True,auto_created=True)
    username=models.ForeignKey(Candidate,on_delete=models.CASCADE)
    title=models.CharField(max_length=20)
    date=models.DateField(auto_now=True)
    time=models.TimeField(auto_now=True)
    right=models.IntegerField()
    time_durations=models.CharField(max_length=50)
    wrong=models.IntegerField()
    points=models.FloatField()
    user_answer_option=models.TextField()
    


    



