from django.db import models

# Create your models here.


class Address(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return (self.name)


class Message(models.Model):
    name = models.CharField(max_length=250)
    text = models.TextField()
    adress = models.ForeignKey(Address, on_delete=models.CASCADE)

    ShowtimeFrom = models.DateTimeField()
    Showtimeto = models.DateTimeField()
    ShowtimeSeconds = models.IntegerField(default=0)

    def __str__(self):
        return (self.name)
