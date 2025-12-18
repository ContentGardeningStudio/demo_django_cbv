from django.db import models

class Order(models.Model):
    name = models.CharField(max_length=100)
    total = models.IntegerField()

    def __str__(self):
        return self.name