from django.db import models


class Classes(models.Model):
    name = models.CharField(max_length=20)
    school = models.CharField(max_length=20)
    description = models.TextField()


class Students(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(blank=True, null=True)
    parent = models.CharField(max_length=30)
    parent_email = models.EmailField()
    photo = models.ImageField(upload_to='/', blank=True, null=True)


class Attendance(models.Model):
    date = models.DateField()
    type = models.CharField(max_length=30)
    student = models.ForeignKey(Students)


class Notes(models.Model):
    date = models.DateField()
    comment = models.TextField()
    student = models.ForeignKey(Students)


class Grades(models.Model):
    subject = models.CharField(max_length=20)
    grade = models.IntegerField()
    type = models.CharField(max_length=20)


class Lessons(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    date = models.DateField()