from django.db import models

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
    

"""

class Student(models.Model):
    name = models.CharField(max_length=255)  # Nome com limite de 255 caracteres
    password = models.CharField(max_length=255)  # Senha com limite de 255 caracteres
    email = models.EmailField(unique=True)  # Email único
    majorId = models.ForeignKey('Curso', on_delete=models.CASCADE)  # Chave estrangeira para Curso
    picture = models.ImageField(upload_to='perfil_aluno/', null=True, blank=True, default=None)

    def __str__(self):
        return self.nome


class Evento(models.Model):
    name = models.CharField(max_length= 255)
    desc_short = models.CharField(max_length= 255)
    desc_detailed = models.CharField(max_length= 511)
    date_begin = models.DateField()
    data_end = models.DateField()
    professorId = models.ForeignKey('Professor', on_delete=models.CASCADE)
    hourTypeId = models.ForeignKey("HourType", on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='fotos/', null=True, blank=True, default=None)
    horaInicio = models.TimeField(default=None)
    horaFim = models.TimeField(default=None)
    def __str__(self):
            return self.nome


class Professor(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    majorId = models.ForeignKey('major', on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='perfil_professor/', null=True, blank=True, default=None)


    def __str__(self):
        return self.nome


class TipoDeHora(models.Model):
    nome_hora = models.CharField(max_length=255)
    horas_max = models.IntegerField()
    horas_max_atv = models.IntegerField()

class HoraComplementar(models.Model):
    horas = models.IntegerField()
    tipoId = models.ForeignKey('TipoDeHora', on_delete=models.CASCADE)
    alunoId = models.ForeignKey('Aluno', on_delete=models.CASCADE)
    certificadoId = models.ForeignKey('Certificado', on_delete=models.CASCADE)

class Certificate(models.Model):
    fs_path = models.CharField(max_length=511)
    studentId = models.ForeignKey('Student', on_delete=models.CASCADE)
    eventId = models.ForeignKey('Event', on_delete=models.CASCADE)

class Registration(models.Model):
    studentId = models.ForeignKey('Student', on_delete=models.CASCADE)
    eventId = models.ForeignKey('Event', on_delete=models.CASCADE)
    #Validar com o pessoal
    qr_code = models.ImageField(upload_to='qr_code/', null=True, blank=True, default=None)


class Presenca(models.Model):
    date = models.DateField()
    status = models.BooleanField(default=None, null=True)
    registrationId = models.ForeignKey('Registration', on_delete=models.CASCADE)
    eventId = models.ForeignKey('Event', on_delete=models.CASCADE)

class principal(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    majorId = models.ForeignKey('Major', on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='perfil_coordenador/', null=True, blank=True, default=None)
    def __str__(self):
        return f"Principal {self.name}"

"""
    