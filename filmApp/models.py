from django.db import models
from django.contrib.auth.models import User
class Aktyor(models.Model):
    ism=models.CharField(max_length=255)
    t_sana=models.DateField(blank=True,null=True)
    davlat=models.CharField(max_length=50)
    jins=models.CharField(max_length=50)

    def __str__(self):
        return self.ism


class Kino(models.Model):
    nom = models.CharField(max_length=255)
    janr = models.CharField(max_length=50)
    yil = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.nom

class KinoAktyor(models.Model):
    kino=models.ForeignKey(Kino,on_delete=models.CASCADE,related_name="kinolar")
    aktyor = models.ForeignKey(Aktyor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.kino.nom}:{self.aktyor}"

class Tarif(models.Model):
    nom=models.CharField(max_length=255)
    davomiylik=models.CharField(max_length=255)
    narx=models.PositiveIntegerField()

    def __str__(self):
        return self.nom

class Izoh(models.Model):
    matn=models.CharField(max_length=255)
    kino= models.ForeignKey(Kino,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.matn[:25]



