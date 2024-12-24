from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


class User(AbstractUser):
  id = models.AutoField(primary_key = True)
  pronombres = [('La', 'La'), ('El', 'El'), ('Le', 'Le'), ('Otro', 'Otro')]
  pronombre = models.CharField(max_length = 5, choices = pronombres)
  apodo = models.CharField(max_length = 30)
  
  def __str__(self):
    return self.first_name + ' ' + self.last_name

class OpinionUser(models.Model):
  id_critico = models.ForeignKey(User, related_name = 'opinion_as_critico', on_delete = models.CASCADE)
  id_criticado = models.ForeignKey(User, related_name = 'opinion_as_criticado', on_delete = models.CASCADE)
  opinion = models.CharField(max_length = 200)
  ratings = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')]
  puntualidad = models.IntegerField(choices = ratings)
  respeto = models.IntegerField(choices = ratings)
  
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete = models.CASCADE)
  bio = models.TextField(max_length = 500, blank = True)
  profile_pic = models.ImageField(default='avatar.jpg',upload_to = 'profile_pics', blank = True)
  def __str__(self):
        return f'{self.user.username} Profile'
  def save(self, *args, **kwargs):
        # save the profile first
        super().save(*args, **kwargs)

        # resize the image
        img = Image.open(self.profile_pic.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            # create a thumbnail
            img.thumbnail(output_size)
            # overwrite the larger image
            img.save(self.profile_pic.path)
  
class Sesion(models.Model):
  Cursos = [('MA1101', 'MA1101'), ('MA1001', 'MA1001'), ('FI1000', 'FI1000'), ('BT1211', 'BT1211'), ('MA1102', 'MA1102'), ('MA1002', 'MA1002'), ('FI1100', 'FI1100'), ('CC1002', 'CC1002'), ('IQ2211', 'IQ2211'), ('FI2001', 'FI2003'), ('MA2001', 'MA2001'), ('IN2201', 'IN2201'), ('IQ2212', 'IQ2212'), ('FI2002', 'FI2002'), ('MA2002', 'MA2002'), ('FI2004', 'FI2004')]
  
  id = models.AutoField(primary_key = True)
  autor = models.CharField(max_length = 30, default = 'Desconocido')
  hora = models.TimeField()
  fecha = models.DateField()
  ramo = models.CharField(max_length = 6, choices=Cursos) #6 equivale a: CC4401 (2 por el departamento) y (4 por el codigo del ramo) quizas sea más
  seccion = models.IntegerField()
  maxMembers = models.IntegerField()
  descripcion = models.CharField(max_length = 200)
  link= models.CharField(max_length = 200)
  members = models.ManyToManyField(User, through='Member', related_name='sesiones_as_member')

class Host(models.Model):
  id_user = models.OneToOneField(User, on_delete = models.CASCADE)
  id_sesion = models.ForeignKey(Sesion, on_delete = models.CASCADE)
  
  def __str__(self):
    return self.id_user.first_name + ' ' + self.id_user.last_name

class Member(models.Model):
  id_user = models.ForeignKey(User, on_delete=models.CASCADE)
  id_host = models.ForeignKey(Sesion, on_delete=models.CASCADE, related_name='sesiones_as_host')
  
  def __str__(self):
    return self.id_user.first_name + ' ' + self.id_user.last_name

class Sala(models.Model):
  sesion = models.ForeignKey(Sesion, on_delete = models.CASCADE)
  #lista de lugares predeterminados para realizar la sesion de estudios: lugares = [.......]
  ubicacion = models.CharField(max_length = 20) #choices=lugares

class OpinionSala(models.Model):
  sala = models.ForeignKey(Sala, on_delete = models.CASCADE)
  #depende si la calificacion es de 1 a 5 o de a 1 a 10, hay que solo modificar esta lista
  ratings = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')]
  ruido = models.CharField(max_length = 2, choices = ratings)
  espacio = models.CharField(max_length = 2, choices = ratings)