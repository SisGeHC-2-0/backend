from django.db import models
import os

# Create your models here.


class Major(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f"Major: {self.name}"
    
class HourType(models.Model):
    name = models.CharField(max_length=100, null=False)
    total_max = models.IntegerField(null=False)
    per_submission_max = models.IntegerField(null=False)

    def __str__(self):
        return f"HourType: {self.name}"
    
class Principal(models.Model):
    email = models.EmailField(unique=True)
    
    
    ## validate the representation of this fields as char
    enrollment_number = models.CharField(max_length=255, unique=True)

    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    majorId = models.ForeignKey('Major', on_delete=models.CASCADE)
    picture = models.ImageField(upload_to= os.sep.join(['images','principal', '']), null=True, blank=True, default=None)
    def __str__(self):
        return f"Principal {self.name}"
    

class Professor(models.Model):
    email = models.EmailField(unique=True)

    ## validate the representation of this fields as char
    enrollment_number = models.CharField(max_length=255, unique=True)

    status= models.BooleanField(default=None, null=True)

    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    majorId = models.ForeignKey('Major', on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=os.sep.join(['images','professor', '']), null=True, blank=True, default=None)


    def __str__(self):
        return f'Professor {self.name}'


class Student(models.Model):
    name = models.CharField(max_length=255)  # Nome com limite de 255 caracteres
    password = models.CharField(max_length=255)  # Senha com limite de 255 caracteres
    email = models.EmailField(unique=True)  # Email único

    ## validate the representation of this fields as char
    enrollment_number = models.CharField(max_length=255, unique=True)


    majorId = models.ForeignKey('Major', on_delete=models.CASCADE)  # Chave estrangeira para Curso
    picture = models.ImageField(upload_to=os.sep.join(['images','professor', '']), null=True, blank=True, default=None)

    def __str__(self):
        return f"Student {self.name}"


class Evento(models.Model):
    name = models.CharField(max_length= 255)
    desc_short = models.CharField(max_length= 255)
    desc_detailed = models.CharField(max_length= 511)
    enroll_date_begin = models.DateField()
    enroll_date_end = models.DateField()
    professorId = models.ForeignKey('Professor', on_delete=models.CASCADE)
    hourTypeId = models.ForeignKey("HourType", on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=os.sep.join(['images','event', '']), null=True, blank=True, default=None)

    workload = models.IntegerField(null= False)

    minimum_attendances = models.IntegerField(null= False)
    maximum_enrollments = models.IntegerField(null= False)

    address = models.CharField(max_length=255, null=False)
    is_online = models.BooleanField(default=False)
    ended = models.BooleanField(default=False, null= False) 
    def __str__(self):
            return self.nome

class EventEnrollment(models.Model):
    studentId = models.ForeignKey('Student', on_delete=models.CASCADE)
    eventId = models.ForeignKey('Event', on_delete=models.CASCADE)

class EventDate(models.Model):
    date = models.DateField()
    time_begin = models.TimeField()
    time_end = models.TimeField()
    eventId = models.ForeignKey('Event', on_delete=models.CASCADE)


class Attendance(models.Model):
    date = models.DateField()
    status = models.BooleanField(default=None, null=True)
    enrollmentId = models.ForeignKey('EventEnrollment', on_delete=models.CASCADE)
    eventId = models.ForeignKey('Event', on_delete=models.CASCADE)

class Certificate(models.Model):
    path = models.CharField(max_length=511)
    studentId = models.ForeignKey('Student', on_delete=models.CASCADE)
    eventId = models.ForeignKey('Event', on_delete=models.CASCADE, null=True)
    
    # Null is true in case it isnt a certificate that we generate
    emission_date = models.DateTimeField(null=True)

    # Some other attributes were described at the concrete model,
    # But it looks like they come from confusion of the Certificate
    # and the HourSubmission tables

class HourSubmission(models.Model):
    workload = models.IntegerField()
    status = models.BooleanField(null=True, default=None)
    description = models.CharField(max_length=500)
    feedback = models.TextField(max_length=500)
    hourTypeId = models.ForeignKey('HourType', on_delete=models.CASCADE)
    tudentId = models.ForeignKey('Student', on_delete=models.CASCADE)
    certificateId = models.ForeignKey('Certificate', on_delete=models.CASCADE)


