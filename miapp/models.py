# miapp/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    us_nombre = models.CharField(max_length=100, blank=False, null=False)
    puntaje_total = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.us_nombre} (@{self.username}) - Puntos: {self.puntaje_total}"

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    ca_nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.ca_nombre

class Dificultad(models.Model):
    id_dificultad = models.AutoField(primary_key=True)
    di_nombre = models.CharField(max_length=50, unique=True)
    puntaje = models.IntegerField(default=10)
    orden = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ["orden"]

    def __str__(self):
        return f"{self.di_nombre} ({self.puntaje} pts)"

class Reto(models.Model):
    id_reto = models.AutoField(primary_key=True)
    re_dificultad = models.ForeignKey(Dificultad, on_delete=models.CASCADE)
    re_categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    re_nombre = models.CharField(max_length=200)
    re_descripcion = models.TextField()
    respuesta_reto = models.CharField(max_length=200)
    intentos = models.IntegerField(default=3)
    re_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='retos_creados', null=True, blank=True) # Nuevo campo para el autor

    def __str__(self):
        return f"{self.re_nombre} ({self.re_dificultad})"

class Respuesta(models.Model):
    id = models.AutoField(primary_key=True)
    res_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    res_reto = models.ForeignKey(Reto, on_delete=models.CASCADE)
    respuesta_usuario = models.CharField(max_length=200)
    respuesta_correcta = models.BooleanField(default=False)
    puntaje = models.IntegerField(default=0)
    intento = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        estado = "Correcta" if self.respuesta_correcta else "Incorrecta"
        return f"{self.res_usuario.us_nombre} - {self.res_reto.re_nombre} - {estado}"

class HistorialPuntaje(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    puntos = models.IntegerField()

    def __str__(self):
        return f"{self.usuario.us_nombre} +{self.puntos}"

class Ranking(models.Model):
    id_ranking = models.AutoField(primary_key=True)
    ra_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    puntaje = models.IntegerField()

    class Meta:
        ordering = ["-puntaje"]

    def __str__(self):
        return f"Ranking {self.ra_usuario.us_nombre}: {self.puntaje} pts"
